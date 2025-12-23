from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from decimal import Decimal, ROUND_HALF_UP
from django.db import models, transaction
import uuid


# Money helper
def quantize_money(value):
    return (Decimal(value) or Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    order_number = models.CharField(max_length=100, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Shipping
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random, string
            self.order_number = 'ORD-SWC-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

    @property
    def payment_status(self):
        """Returns the status of the most recent payment."""
        latest_payment = self.payments.order_by('-created_at').first()
        return latest_payment.status if latest_payment else 'No Payment'
    

    def calculate_totals(self):
        subtotal = sum([item.get_subtotal() for item in self.items.all()])
        self.subtotal = quantize_money(subtotal)
        self.total = quantize_money(self.subtotal + self.shipping_cost + self.tax)
        self.save()



class OrderItem(models.Model):
    # Link to the Order using a string reference to avoid circular imports
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, null=True, blank=True)
    product_name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)  # Naira
    quantity = models.PositiveIntegerField(default=1)

    replace_product_sku = models.CharField(max_length=64, blank=True, null=True)
    replace_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} for Order {self.order.order_number}"
    
    def get_subtotal(self):
        return quantize_money(self.price * Decimal(self.quantity))



