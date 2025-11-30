from django.core.management.base import BaseCommand
from products.models import Product, Category
from decimal import Decimal
import random


PRODUCTS = [
    {
        "name": "Samsung Galaxy S23",
        "category": "Electronics",
        "description": "Latest Samsung flagship smartphone.",
        "price": 580000,
    },
    {
        "name": "Tecno Spark 10 Pro",
        "category": "Electronics",
        "description": "Affordable smartphone with strong battery life.",
        "price": 145000,
    },
    {
        "name": "Adidas Men's Running Shoes",
        "category": "Fashion",
        "description": "Durable and lightweight running shoes.",
        "price": 42000,
    },
    {
        "name": "Nivea Body Lotion",
        "category": "Beauty",
        "description": "Smooth and revitalizing body lotion.",
        "price": 3500,
    },
    {
        "name": "Wooden Study Desk",
        "category": "Furniture",
        "description": "Compact wooden study desk.",
        "price": 65000,
    },
    {
        "name": "Binatone Electric Blender",
        "category": "Home Appliances",
        "description": "High-quality multifunctional blender.",
        "price": 28000,
    },
    {
        "name": "HP Pavilion Laptop (Core i5)",
        "category": "Computers",
        "description": "Powerful laptop for work and learning.",
        "price": 430000,
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample product data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding product data...")

        for item in PRODUCTS:
            category_name = item["category"]
            category, _ = Category.objects.get_or_create(name=category_name)

            Product.objects.create(
                name=item["name"],
                category=category,
                description=item["description"],
                price=Decimal(item["price"]),
                in_stock=random.randint(3, 20),  # simulate stock
                is_published=True,
            )

        self.stdout.write(self.style.SUCCESS("Products seeded successfully!"))
