from django.db import models
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField(default=0)

    brand = models.CharField(max_length=120, blank=True, null=True)
    rating = models.FloatField(default=0)
    total_views = models.IntegerField(default=0)

    flash_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    flash_sale_ends_at = models.DateTimeField(blank=True, null=True)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def final_price(self):
        """Return the final price considering flash sale"""
        from django.utils import timezone

        # Check if flash sale is active
        if (
            self.flash_price is not None and
            self.flash_sale_ends_at is not None and
            timezone.now() < self.flash_sale_ends_at
        ):
            return self.flash_price
        return self.price

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

