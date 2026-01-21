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
from .utils.cache_manager import CacheManager

# Category List and Create
@extend_schema(tags=["Products"])
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


# Product List and Create
@extend_schema(tags=["Products"])
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    # Filtering and searching
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Search fields for filtering
    search_fields = ['name', 'brand', 'category__name']
    ordering_fields = ['price', 'rating', 'created_at']

    # Cache manager config for product list
    cache_manager = CacheManager(prefix="products", timeout=300)

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated and user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_published=True)
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    # List products with caching
    def list(self, request, *args, **kwargs):

        user = request.user
        page_number = request.query_params.get('page', '1')
        identifier = f"products_staff_page_{page_number}" if (user.is_authenticated and user.is_staff) else f"products_public_page_{page_number}"

        cached_data = self.cache_manager.get(identifier)
        if cached_data:
            response = Response(cached_data)
            response["X-Cache"] = "HIT"
            return response

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = serializer.data

        paginated_response = self.get_paginated_response(data)

        self.cache_manager.set(identifier, paginated_response.data)
        paginated_response["X-Cache"] = "MISS"

        return paginated_response
    
    # invalidate cache to fetch latedt data from the DB
    def perform_create(self, serializer):
        serializer.save()
        self.cache_manager.invalidate()


# Product Detail for Admin
@extend_schema(tags=["Products"])
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    cache_manager = CacheManager(prefix="products", timeout=300)

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def retrieve(self, request, *args, **kwargs):
        product_id = self.kwargs.get(self.lookup_field or 'pk')
        cache_key = f"product_{product_id}"

        cached_data = self.cache_manager.get(cache_key)
        if cached_data:
            response = Response(cached_data)
            response["X-Cache"] = "HIT"
            return response

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        self.cache_manager.set(cache_key, data)
        response = Response(data)
        response["X-Cache"] = "MISS"
        return response

    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate cache for this product after update
        product_id = instance.pk
        cache_key = f"product_{product_id}"
        self.cache_manager.invalidate(cache_key)

    def perform_destroy(self, instance):
        product_id = instance.pk
        instance.delete()
        # Invalidate cache for this product after deletion
        cache_key = f"product_{product_id}"
        self.cache_manager.invalidate(cache_key)


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