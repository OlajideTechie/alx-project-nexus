from rest_framework import generics, permissions, filters, status

from authentication.models import User
from .models import Product, Category
from .serializers.serializers import ProductSerializer, CategorySerializer, AdminProductSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from common.permissions import IsAdmin
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import viewsets


@extend_schema(tags=["Products"])
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(tags=["Products"])
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand', 'category__name']
    ordering_fields = ['price', 'rating', 'created_at']

    def get_queryset(self):
        # Admin users see all products; others only see published
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated and user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(tags=["Products"])
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    

@extend_schema(tags=["Admin Management"])
class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        product = self.get_object()
        product.is_published = True
        product.save()
        return Response({"message": "Product published"})

    @action(detail=True, methods=["post"])
    def unpublish(self, request, pk=None):
        product = self.get_object()
        product.is_published = False
        product.save()
        return Response({"message": "Product unpublished"})

    @action(detail=False, methods=["post"])
    def seed(self, request):
        # Seed the database with initial product data in an array format
        initial_data = [
            {
                "name": "Product 1",
                "description": "Description for Product 1",
                "price": 100.00,
                "category": "55bbebbfd5c14a3aac5b0680a5738469",
                "brand": "Br",
                "in_stock": 20,
                "is_published": True
            },
            {
                "name": "Product 2",
                "description": "Description for Product 2",
                "price": 150.00,
                "category": "55bbebbfd5c14a3aac5b0680a5738469",
                "brand": "Brand 2",
                "in_stock": 10,
                "is_published": True
            },
            {
                "name": "Product 3",
                "description": "Description for Product 3",
                "price": 200.00,
                "category": "55bbebbfd5c14a3aac5b0680a5738469",
                "brand": "Brand 3",
                "in_stock": 5,
                "is_published": True
            }
        ]

        serializer = self.get_serializer(data=initial_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Products seeded successfully"}, status=201)