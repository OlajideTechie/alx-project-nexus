from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, VerifyPaymentViewSet, paystack_callback

app_name = 'payments'


urlpatterns = [
    path("initiate", PaymentViewSet.as_view({'post': 'initiate'}), name="initiate-payment"),
    path("verify", VerifyPaymentViewSet.as_view({'get': 'verify'}), name="verify-payment"),
    path("paystack/callback", paystack_callback, name="paystack-callback"),
]