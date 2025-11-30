from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from .services import OrderService

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'price', 'quantity', 'replace_product_sku', 'replace_notes']
        read_only_fields = ['id', 'product_name', 'price']

class OrderCreateItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    replace_product_sku = serializers.CharField(required=False, allow_blank=True)
    replace_notes = serializers.CharField(required=False, allow_blank=True)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment_status = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'payment_status',
            'shipping_address', 'shipping_city', 'shipping_state',
            'shipping_country', 'shipping_postal_code', 'phone_number',
            'subtotal', 'shipping_cost', 'tax', 'total',
            'notes', 'items', 'created_at'
        ]
        read_only_fields = ['id', 'order_number', 'status', 'created_at', 'subtotal', 'total']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderCreateItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'shipping_address', 'shipping_city', 'shipping_state',
            'shipping_country', 'shipping_postal_code', 'phone_number',
            'notes', 'items'
        ]

    def validate(self, attrs):
        if not attrs.get('items'):
            raise serializers.ValidationError("Order must contain at least one item.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        service = OrderService(user=user, order_data=validated_data)
        try:
            order = service.create_order()
        except ValueError as e:
            raise serializers.ValidationError({"items": e.args[0]})
        return order
