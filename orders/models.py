import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Prevent deletion if user has orders
        related_name="orders"
    )

    order_number = models.CharField(max_length=32, unique=True, db_index=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    # ---- Price snapshot totals ----
    subtotal = models.DecimalField(max_digits=12, decimal_places=2) # Sum of item prices before tax and shipping
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0) # Final amount charged

    # ----- Shipping info (snapshot) -----
    shipping_address = models.TextField(max_length=500, default='123, Main Street, City, Country')
    phone_number = models.CharField(max_length=20, default='234567890')

    # ---- Price lock window ----
    price_locked_until = models.DateTimeField(null=True, blank=True)

    # ---- Audit ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["status", "payment_status"]),
        ]

    # String representation, price lock methods
    def __str__(self):
        return f"Order {self.order_number}"

    # Check if price lock is active
    def is_price_lock_active(self):
        return self.price_locked_until and timezone.now() <= self.price_locked_until


#  Order Item Model
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    # ---- Snapshot fields ----
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ("order", "product")
        indexes = [
            models.Index(fields=["order"]),
        ]

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"
