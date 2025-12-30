from time import timezone
import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart
from .serializers import OrderSerializer, CreateOrderSerializer
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


@extend_schema(tags=['Orders'],)
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    """Ensures users only see their own orders."""
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Create order from cart"""
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart = get_object_or_404(Cart, user=request.user)

        # Ensure cart is active and has items befrore creating order
        try:
            cart = get_object_or_404(Cart, user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Active Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if cart has items
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        lock_duration = timedelta(minutes=15)

        # Create order within a transaction
        with transaction.atomic():
            # Calculate subtotal for order
            subtotal = sum(
                cart_item.product.price * cart_item.quantity 
                for cart_item in cart.items.all()
            )

            TAX_RATE = Decimal("0.01")
            tax = subtotal * TAX_RATE
            shipping_cost = Decimal("0.00")
            total_amount = subtotal + shipping_cost + tax
            
            # Create order
            order = Order.objects.create(

                    user=request.user,
                    order_number=f"ORD_SWC-{uuid.uuid4().hex[:10].upper()}",
                    subtotal=subtotal,
                    tax=tax,
                    total_amount=total_amount,          
                    price_locked_until=timezone.now() + lock_duration,
                    shipping_address=serializer.validated_data.get(
                        "shipping_address", "123 Main Street"
                    ),
                    phone_number=serializer.validated_data.get("phone_number", "234567890")

            )
            
            # Create order items from cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.price
                )
            
            # Clear the cart after order creation
            cart.is_active = False
            cart.save(update_fields=['is_active'])
            
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.status in ['shipped', 'delivered']:
            return Response(
                {'error': 'Cannot cancel order that has been shipped or delivered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.status == 'cancelled':
            return Response(
                {'error': 'Order is already cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Restore stock
            for item in order.items.all():
                product = item.product
                product.stock_quantity += item.quantity
                product.save()
            
            order.status = 'cancelled'
            order.save()
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )
