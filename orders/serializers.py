from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "product_name",
            "unit_price",
            "quantity"
        ]

        read_only_fields = ["product_name", "unit_price", "line_total"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "tax",
            "shipping_address",
            "payment_status",
            "status",
            "phone_number",
            "items",
            "price_locked_until",
            "subtotal",
            "total_amount",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "order_number",
            "tax",
            "total",
            "status",
            "created_at",
            "items",
            "price_locked_until"
        ]
        def get_is_price_lock_active(self, obj):
            return obj.is_price_lock_active()
        
# Serializer for order creation input
class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)