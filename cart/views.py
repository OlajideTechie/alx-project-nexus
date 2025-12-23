from email.mime import message
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product

from .serializers import (CartSerializer, 
                          RemoveCartItemSerializer, 
                          AddCartItemSerializer, 
                          UpdateCartItemSerializer,
                          ClearCartSerializer)


from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema

# ViewSet for managing the shopping cart

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    # Retrieve the current user's cart
    
    @extend_schema(
        tags=["Carts"],
        responses={200: CartSerializer},
        description="Retrieve the authenticated user's cart."
    )
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # Add a product to the cart
    @extend_schema(
        tags=["Carts"],
        request=AddCartItemSerializer,
        responses={200: CartSerializer},
        examples=[
            OpenApiExample(
                name="Add Product to Cart",
                value={
                    "product_id": "9e8d3c64-8a34-4b2b-9bdf-9e2b1cdb11aa",
                    "quantity": 2
                },
                request_only=True,
            )
        ],
        description="Add a product to the cart or increase its quantity."
    )

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the product and check its availability
        product = get_object_or_404(
            Product,
            id=product_id,
            is_published=True,
            in_stock__gt=0, # stock is greater than 0, meaning available
        )
        
        # Check stock availability
        if quantity > product.in_stock:
            return Response({'error': 'Insufficient stock, available quantity is ' + str(product.in_stock)}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        # Update quantity if item already exists in cart
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.in_stock:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        # Return the updated cart, serialized
        serializer = CartSerializer(cart)
        return Response(
            {
                "message": "Item added to cart successfully",
                **serializer.data
         },
        status=status.HTTP_200_OK
    )


    # Update the quantity of an item in the cart
    @extend_schema(
        tags=["Carts"],
        request=UpdateCartItemSerializer,
        responses={200: CartSerializer},
        examples=[
            OpenApiExample(
                name="Update Cart Item Quantity",
                value={
                    "item_id": "0f7c3a52-3e98-4c2f-a1b4-2c9f2a4cfa12",
                    "quantity": 3
                },
                request_only=True,
            )
        ],
        description="Update the quantity of an item in the cart. Set quantity to 0 to remove it."
    )
    @action(detail=False, methods=['patch'])
    def update_item(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        if not item_id or quantity is None:
            return Response({'error': 'item_id and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if int(quantity) > cart_item.product.in_stock:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(quantity) <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(
            {
                "message": "Cart item updated successfully",
                **serializer.data
            },
            status=status.HTTP_200_OK
        )

    # Remove an item from the cart
    @extend_schema(
        tags=["Carts"], 
        request=RemoveCartItemSerializer,
        responses={200: CartSerializer},
        examples=[
            OpenApiExample(
                name="Remove Cart Item",
                value={
                    "item_id": "0f7c3a52-3e98-4c2f-a1b4-2c9f2a4cfa12"
                },
                request_only=True,
            )
        ],
        description="Remove an item from the cart."
    )
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response({'error': 'item_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()

        return Response(
            {
                "message": "Item removed from cart successfully",

            },
            status=status.HTTP_200_OK
        )

    # Clear all items from the cart
    @extend_schema(
        tags=["Carts"],
        responses={200: ClearCartSerializer},
        description="Clear all items from the cart.",
        examples=[
            OpenApiExample(
                name="Clear Cart",
                value={},
                request_only=True,
            )
        ]
    )
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        
        return Response(
            {
                "message": "Cart cleared successfully",

            },
            status=status.HTTP_200_OK
        )