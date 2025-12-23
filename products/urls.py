from django.urls import path
from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    ProductDetailView,
    ProductPublishToggleView,
)

app_name = 'products'

urlpatterns = [
    path('categories', CategoryListCreateView.as_view()),
    path('', ProductListCreateView.as_view()),
    path('<uuid:pk>', ProductDetailView.as_view()),
    path('<uuid:pk>/toggle-publish', ProductPublishToggleView.as_view(), name="product-toggle-publish"),
]