from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum, Count
from drf_spectacular.utils import extend_schema

from authentication.models import User
from products.models import Product
from orders.models import Order, OrderItem

@extend_schema(tags=["Analytics"])
class AdminDashboardAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        analytics = {
            "total_users": User.objects.count(),
            "verified_users": User.objects.filter(is_verified=True).count(),
            "total_products": Product.objects.count(),
            "published_products": Product.objects.filter(is_published=True).count(),
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status='pending').count(),
            "processing_orders": Order.objects.filter(status='processing').count(),
            "shipped_orders": Order.objects.filter(status='shipped').count(),
            "total_revenue": Order.objects.aggregate(total=Sum("total_amount"))["total"] or 0,
            "top_selling_products": (
                OrderItem.objects.values("product__name")
                .annotate(total_sold=Sum("quantity"))
                .order_by("-total_sold")[:5]
            ),
            "orders_last_7_days": (
                Order.objects
                .extra({"created_at_date": "DATE(created_at)"})
                .values("created_at_date")
                .annotate(count=Count("id"))
                .order_by("created_at_date")[:7]
            ),
        }

        return Response({"status": "success", "data": analytics})
