from django.urls import path, include
from .views import CartViewSet

app_name = 'cart'

urlpatterns = [
    path('', include(([
        path('', CartViewSet.as_view({'get': 'list'}), name='cart-detail'),
        path('add-item', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
        path('update-item', CartViewSet.as_view({'patch': 'update_item'}), name='cart-update-item'),
        path('remove-item', CartViewSet.as_view({'delete': 'remove_item'}), name='cart-remove-item'),
        path('empty', CartViewSet.as_view({'delete': 'clear'}), name='cart-clear'),
    ], 'cart'), namespace='cart')),
]