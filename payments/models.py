from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    order = models.ForeignKey("orders.Order", related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    provider = models.CharField(max_length=50, default='paystack')  # for paystack
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)  # save gateway metadata here

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"
