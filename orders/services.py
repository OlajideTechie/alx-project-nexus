# orders/services.py

from django.db import transaction
from products.models import Product
from decimal import Decimal
from .models import Order, OrderItem
from decimal import Decimal
from orders.models import quantize_money 


class OrderService:
    def __init__(self, user, order_data):
        self.user = user
        self.order_data = order_data
        self.errors = []

    def validate_items(self, items):
        if not items:
            self.errors.append("Order must contain at least one item.")
            return False

        for item in items:
            try:
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                self.errors.append(f"Product with ID {item['product_id']} does not exist.")
                continue

            if item['quantity'] < 1:
                self.errors.append(f"Quantity for product {product.name} must be at least 1.")
            
            # Example stock check (adjust as per your product model)
            if hasattr(product, 'stock') and product.stock < item['quantity']:
                self.errors.append(f"Insufficient stock for product {product.name}.")

        return len(self.errors) == 0

    @transaction.atomic
    def create_order(self):
        items_data = self.order_data.pop('items', [])
        if not self.validate_items(items_data):
            raise ValueError(self.errors)

        order = Order.objects.create(user=self.user, **self.order_data)

        subtotal = Decimal('0')

        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=item['quantity'],
                replace_product_sku=item.get('replace_product_sku'),
                replace_notes=item.get('replace_notes')
            )
            subtotal += order_item.get_subtotal()

        order.subtotal = quantize_money(subtotal)
        order.total = quantize_money(order.subtotal + order.shipping_cost + order.tax)
        order.save()

        return order
