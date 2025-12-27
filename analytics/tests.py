import datetime
from django.urls import reverse
from django.utils import timezone
import pytest
from rest_framework.test import APIClient
from authentication.models import User
from products.models import Product
from orders.models import Order, OrderItem


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(email="admin@example.com", password="pass1234", username="admin")


@pytest.fixture
def api_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def endpoint():
    return reverse("analytics:admin-dashboard")


@pytest.mark.django_db
def test_unauthenticated_request_is_forbidden(client, endpoint):
    res = client.get(endpoint)
    assert res.status_code in (401, 403)


@pytest.mark.django_db
def test_counts_with_empty_database(api_client, endpoint):
    res = api_client.get(endpoint)
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_users"] == 1  # only admin exists
    assert data["verified_users"] == 0
    assert data["total_products"] == 0
    assert data["published_products"] == 0
    assert data["total_orders"] == 0
    assert data["pending_orders"] == 0
    assert data["processing_orders"] == 0
    assert data["shipped_orders"] == 0
    assert data["total_revenue"] == 0
    assert data["top_selling_products"] == []
    assert data["orders_last_7_days"] == []


@pytest.mark.django_db
def test_product_and_order_aggregations(api_client, endpoint):
    # products
    p1 = Product.objects.create(name="P1", price=10, is_published=True)
    p2 = Product.objects.create(name="P2", price=20, is_published=False)

    # orders
    o1 = Order.objects.create(status="pending", total_amount=100)
    o2 = Order.objects.create(status="processing", total_amount=50)
    o3 = Order.objects.create(status="shipped", total_amount=0)

    OrderItem.objects.create(order=o1, product=p1, quantity=3)
    OrderItem.objects.create(order=o1, product=p2, quantity=1)
    OrderItem.objects.create(order=o2, product=p1, quantity=2)

    res = api_client.get(endpoint)
    assert res.status_code == 200
    data = res.json()["data"]

    assert data["total_products"] == 2
    assert data["published_products"] == 1

    assert data["total_orders"] == 3
    assert data["pending_orders"] == 1
    assert data["processing_orders"] == 1
    assert data["shipped_orders"] == 1

    assert data["total_revenue"] == 150

    top = data["top_selling_products"]
    # P1 sold 5, P2 sold 1
    assert top[0]["product__name"] == "P1"
    assert top[0]["total_sold"] == 5


@pytest.mark.django_db
def test_orders_last_7_days_grouping(api_client, endpoint):
    # create orders on different days
    now = timezone.now()
    # Helper to set created_at if model has auto_add; we update field directly
    def make_order(days_ago: int):
        o = Order.objects.create(status="pending", total_amount=10)
        Order.objects.filter(pk=o.pk).update(created_at=now - datetime.timedelta(days=days_ago))
        return Order.objects.get(pk=o.pk)

    make_order(0)
    make_order(1)
    make_order(1)
    make_order(6)
    make_order(7)  # this one may be excluded depending on slice [:7]

    res = api_client.get(endpoint)
    assert res.status_code == 200
    data = res.json()["data"]

    # Ensure counts grouped by date exist and are ordered
    dates = [entry["created_at_date"] for entry in data["orders_last_7_days"]]
    counts = [entry["count"] for entry in data["orders_last_7_days"]]
    assert sorted(dates) == dates
    assert sum(counts) >= 4


@pytest.mark.django_db
def test_only_admin_has_access(client, endpoint):
    # regular user
    user = User.objects.create_user(email="user@example.com", password="pass1234", username="user")
    client.force_authenticate(user=user)
    res = client.get(endpoint)
    assert res.status_code in (401, 403)
