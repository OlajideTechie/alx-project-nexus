import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from products.models import Product, Category
from cart.models import Cart, CartItem

User = get_user_model()

"""
Tests for Cart functionality.
"""

"""Tests for adding an item to the cart."""
@pytest.mark.django_db
def test_add_item_to_cart():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=10,
        is_published=True
    )

    response = client.post('/api/cart/add-item', {
        "product_id": product.id,
        "quantity": 2
    })

    assert response.status_code == 200
    assert CartItem.objects.count() == 1
    assert CartItem.objects.first().product == product
    assert CartItem.objects.first().quantity == 2


"""Tests for updating cart item quantity."""
@pytest.mark.django_db
def test_update_cart_item_quantity():   
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=10,
        is_published=True
    )

    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)

    response = client.patch('/api/cart/update-item', {
        "item_id": str(cart_item.id),
        "quantity": 5
    })

    assert response.status_code == 200
    cart_item.refresh_from_db()
    assert cart_item.quantity == 5


"""Tests for removing an item from the cart."""
@pytest.mark.django_db
def test_remove_item_from_cart():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=10,
        is_published=True
    )

    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)

    response = client.delete('/api/cart/remove-item', {
        "item_id": str(cart_item.id)
    })

    assert response.status_code == 200
    assert CartItem.objects.count() == 0


"""Tests for clearing the cart."""
@pytest.mark.django_db
def test_clear_cart():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product1 = Product.objects.create(
        category=category,
        name="Test Product 1",
        price=100,
        in_stock=10,
        is_published=True
    )

    product2 = Product.objects.create(
        category=category,
        name="Test Product 2",
        price=150,
        in_stock=5,
        is_published=True
    )

    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product=product1, quantity=2)
    CartItem.objects.create(cart=cart, product=product2, quantity=1)

    response = client.delete('/api/cart/empty')

    assert response.status_code == 200
    assert CartItem.objects.count() == 0


"""Tests for retrieving the cart."""
@pytest.mark.django_db
def test_retrieve_cart():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=10,
        is_published=True
    )

    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product=product, quantity=2)

    response = client.get('/api/cart/')

    assert response.status_code == 200
    assert response.data['total_items'] == 1
    assert response.data['subtotal'] == "200.00"


"""Tests for adding item exceeding stock."""
@pytest.mark.django_db
def test_add_item_exceeding_stock():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=5,
        is_published=True
    )

    response = client.post('/api/cart/add-item', {
        "product_id": product.id,
        "quantity": 10
    })

    assert response.status_code == 400
    assert 'Insufficient stock' in response.data['error']


"""Tests for updating item exceeding stock."""
@pytest.mark.django_db
def test_update_item_exceeding_stock():  
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=5,
        is_published=True
    )

    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)

    response = client.patch('/api/cart/update-item', {
        "item_id": str(cart_item.id),
        "quantity": 10
    })

    assert response.status_code == 400
    assert 'Insufficient stock' in response.data['error']


"""Tests for updating item to zero quantity (removal)."""
@pytest.mark.django_db
def test_update_item_to_zero_quantity():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=10,
        is_published=True
    )

    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)

    response = client.patch('/api/cart/update-item', {
        "item_id": str(cart_item.id),
        "quantity": 0
    })

    assert response.status_code == 200
    assert CartItem.objects.count() == 0


"""Tests for retrieving an empty cart."""
@pytest.mark.django_db
def test_retrieve_empty_cart():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    response = client.get('/api/cart/')

    assert response.status_code == 200
    assert response.data['total_items'] == 0
    assert response.data['subtotal'] == "0.00"


"""Test for adding item with missing product_id."""
@pytest.mark.django_db
def test_add_item_with_missing_product_id():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    response = client.post('/api/cart/add-item', {
        "quantity": 2
    })

    assert response.status_code == 400
    assert 'product_id' in response.data['error']


"""Test for updating item with missing quantity."""
@pytest.mark.django_db
def test_update_item_with_missing_quantity():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Electronics")

    product = Product.objects.create(
        category=category,
        name="Test Product",
        price=100,
        in_stock=10,
        is_published=True
    )

    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)

    response = client.patch('/api/cart/update-item', {
        "item_id": str(cart_item.id)
    })

    assert response.status_code == 400
    assert 'quantity' in response.data['error']


""" Test for adding an item with an invalid product_id."""
@pytest.mark.django_db
def test_add_item_with_invalid_product_id():
    client = APIClient()
    user = User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpass'
    )
    client.force_authenticate(user=user)

    response = client.post('/api/cart/add-item', {
        "product_id": "00000000-0000-0000-0000-000000000000",
        "quantity": 2
    })

    assert response.status_code == 404
    assert 'No Product matches the given query.' in response.data['detail']