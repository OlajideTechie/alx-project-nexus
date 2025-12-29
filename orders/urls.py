# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

app_name = 'orders'

urlpatterns = [
    path('', include(DefaultRouter().urls)),
    path('create', OrderViewSet.as_view({'post': 'create_order'}), name='create-order'),
    path('<uuid:pk>', OrderViewSet.as_view({'get': 'retrieve'}), name='order-detail'),
    path('orders', OrderViewSet.as_view({'get': 'list'}), name='order-list'),
    path('<uuid:pk>/cancel', OrderViewSet.as_view({'post': 'cancel'}), name='cancel-order')
]