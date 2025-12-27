# cart/serializers.py
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Cart, CartItem
from products.serializers.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            'id', 'product', 'product_id', 'quantity',
            'total_price', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'total_price')

    @extend_schema_field(OpenApiTypes.DECIMAL) 
    def get_total_price(self, obj) -> str:
        """
        Returns line total as a string with 2 decimal places (common for money)
        """
        total = obj.quantity * obj.product.price
        return f"{total:.2f}"  # return total if price is Decimal


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    # These are computed on the model (or via properties/methods)
    total_items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id', 'items', 'total_items', 'subtotal',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_items(self, obj) -> int:
        return obj.items.count()

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_subtotal(self, obj) -> str:
        total = sum(
            item.quantity * item.product.price
            for item in obj.items.all()
        )
        return f"{total:.2f}"


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def to_representation(self, instance):
        return super().to_representation(instance)


class UpdateCartItemSerializer(serializers.Serializer):
    item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=0, allow_null=False)


class RemoveCartItemSerializer(serializers.Serializer):
    item_id = serializers.UUIDField()

    @extend_schema_field(OpenApiTypes.UUID)
    def to_representation(self, instance):
        return super().to_representation(instance)


class ClearCartSerializer(serializers.Serializer):
    pass