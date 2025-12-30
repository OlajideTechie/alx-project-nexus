import random
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import uuid
from django.shortcuts import redirect
from django.conf import settings
import requests
from django.db import transaction
from cart.models import Cart
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes

from .models import Payment
from .serializers import (
    PaymentSerializer,
    InitiatePaymentSerializer,
    RetryPaymentSerializer,
)
from orders.models import Order

@extend_schema(tags=['Payments'])
class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_serializer_class(self):
        if self.action == "initiate":
            return InitiatePaymentSerializer
        return self.serializer_class

    @action(detail=False, methods=["post"])
    def initiate(self, request):
        # Validate request
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]

        # Fetch the order
        order = Order.objects.filter(id=order_id, user=request.user).first()
        if not order:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if order has expired
        if timezone.now() > order.price_locked_until:
            order.status = "expired"
            order.save(update_fields=["status"])
            return Response(
                {"error": "Order has expired. Please create a new order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure order is still pending
        if order.status.lower() != "pending":
            return Response(
                {"error": f"Order cannot be paid for (current status: {order.status})"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reference = f"PAY-{uuid.uuid4().hex[:12]}"



        # Resolve previous payment attempts
        Payment.objects.filter(
        order=order,
        status="initiated"
        ).update(status="failed")

        # Create internal Payment record
        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.total_amount,  # snapshot amount
            reference=reference,
            status="initiated"
        )

        # Build callback URL
        callback_url = request.build_absolute_uri(reverse("payments:paystack-callback"))

        # Prepare Paystack payload
        payload = {
            "email": request.user.email,
            "amount": int(order.total_amount * 100),  # Paystack expects kobo
            "reference": str(payment.reference),
            "callback_url": callback_url,
        }

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        # Initialize Paystack transaction
        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            json=payload,
            headers=headers,
            timeout=30,
        )
        data = response.json()

        if not data.get("status"):
            return Response({"error": "Payment initialization failed"}, status=status.HTTP_400_BAD_REQUEST)

        # Save authorization URL
        payment.raw_response = data["data"]["authorization_url"]
        payment.save(update_fields=["raw_response"])

        # Return result
        return Response(
            {
                "authorization_url": payment.raw_response,
                "reference": payment.reference
            },
            status=status.HTTP_200_OK
        )
    

@extend_schema(tags=['Payments'])
class VerifyPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def verify(self, request):
        reference = request.query_params.get("reference")

        payment = get_object_or_404(Payment, reference=reference)

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        response = requests.get(
            f"https://api.paystack.co/transaction/verify/{reference}",
            headers=headers,
        )

        data = response.json()

        if data["data"]["status"] == "success":
            payment.status = "successful"
            payment.gateway_response = data
            payment.save()

            order = payment.order
            order.payment_status = "completed"
            order.status = "processing"
            order.save(update_fields=["payment_status", "status"])

            return Response({"message": "Payment successful"})

        payment.status = "failed"
        payment.gateway_response = data
        payment.save()

        return Response({"message": "Payment failed"})


def verify_paystack_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    data = resp.json()
    return data

@extend_schema(tags=['Payments'])
@api_view(["GET"])
@permission_classes([AllowAny])  # Paystack will not send auth headers
def paystack_callback(request):
    reference = request.GET.get("reference")

    if not reference:
        return Response(
            {"error": "Payment reference not provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Fetch payment object
    try:
        payment = Payment.objects.select_related("order", "user").get(
            reference=reference
        )
    except Payment.DoesNotExist:
        return Response(
            {"error": "Payment not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Idempotency check (Paystack may retry callback)
    if payment.status == "success":
        return Response(
            {"message": "Payment already processed"},
            status=status.HTTP_200_OK
        )

    # Verify payment with Paystack
    result = verify_paystack_payment(reference)

    if not result.get("status") or result["data"]["status"] != "success":
        payment.status = "failed"
        payment.save(update_fields=["status"])
        return Response(
            {"status": "failed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ---- PAYMENT SUCCESSFUL ----
    with transaction.atomic():
        payment.status = "success"
        payment.save(update_fields=["status"])

        order = payment.order
        order.payment_status = "completed"
        order.status = "processing"
        order.save(update_fields=["payment_status", "status"])

        # Clear user's active cart
        cart = (
            Cart.objects
            .filter(user=payment.user, is_active=True)
            .prefetch_related("items")
            .first()
        )

        if cart:
            cart.items.all().delete()
            cart.is_active = False
            cart.save(update_fields=["is_active"])

    return Response(
        {
            "status": "success",
            "order_id": str(order.id),
            "message": "Payment successful and cart cleared"
        },
        status=status.HTTP_200_OK
    )