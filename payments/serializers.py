from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "order",
            "amount",
            "reference",
            "status",
            "authorization_url",
            "gateway_response",
            "created_at",
        )
        read_only_fields = fields

class InitiatePaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()


class RetryPaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()