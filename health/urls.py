from django.urls import path
from .views import HealthCheck, db_health


urlpatterns = [
    #path("health/", HealthCheck.as_view(), name="health"),
    path("health/", db_health, name="db-health"),
]
