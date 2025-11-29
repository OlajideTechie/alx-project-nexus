from rest_framework import generics, permissions, filters, status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


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


@extend_schema(tags=["Products"])
class ProductPublishToggleView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product.is_published = not product.is_published
        product.save(update_fields=["is_published"])

        state = "published" if product.is_published else "unpublished"

        return Response({
            "message": f"Product has been {state} successfully.",
            "product_id": str(product.id),
            "is_published": product.is_published
        })