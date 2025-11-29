from django.urls import path
from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    ProductDetailView,
    ProductPublishToggleView,
)

app_name = 'products'

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('products/', ProductListCreateView.as_view()),
    path('products/<uuid:pk>/', ProductDetailView.as_view()),
    path('products/<uuid:pk>/toggle-publish/', ProductPublishToggleView.as_view(), name="product-toggle-publish"),
]