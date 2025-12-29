from django.urls import path
from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    ProductDetailView,
    AdminProductViewSet
)

app_name = 'products'

urlpatterns = [
    path('categories', CategoryListCreateView.as_view()),
    path('', ProductListCreateView.as_view()),
    path('<uuid:pk>', ProductDetailView.as_view()),
    path('admin-products/seed', AdminProductViewSet.as_view({'post': 'seed'}), name="seed-admin-products"),
    path('admin-products/<uuid:pk>/publish', AdminProductViewSet.as_view({'post': 'publish'}), name="admin-publish-product"),
    path('admin-products/<uuid:pk>/unpublish', AdminProductViewSet.as_view({'post': 'unpublish'}), name="admin-unpublish-product"),
]