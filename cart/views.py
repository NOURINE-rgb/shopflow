from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from products.models import Product

from .serializers import AddToCartSerializer, UpdateCartItemSerializer

# Create your views here.


@extend_schema(
    tags=["Cart"],
    responses={200: dict},
)
class CartDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = [
            {
                "id": item.id,
                "product": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "total": item.price * item.quantity,
            }
            for item in cart.items.all()
        ]
        total_price = sum(item["total"] for item in items)
        return Response({"items": items, "total_price": total_price})


@extend_schema(
    tags=["Cart"],
    request=AddToCartSerializer,
    responses={200: dict},
)
class AddToCartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        product = Product.objects.get(id=product_id)
        if quantity > product.stock:
            return Response(
                {"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = cart.items.get_or_create(
            cart=cart,
            product=product,
            default={
                "quantity": quantity,
                "price": product.discounted_price or product.price,
            },
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response({"detail": "Product added to cart"})


@extend_schema(
    tags=["Cart"],
    request=UpdateCartItemSerializer,
    responses={200: dict},
)
class UpdateCartItemApiView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateCartItemSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        cart_item_id = serializer.validated_data["cart_item_id"]
        quantity = serializer.validated_data["quantity"]
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"detail": "Cart item updated"})


@extend_schema(
    tags=["Cart"],
    responses={204: None},
)
class RemoveCartItemApiView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_item_id):
        cart_item = CartItem.objects.get_object_or_404(
            id=cart_item_id, cart__user=request.user
        )
        cart_item.delete()
        return Response(
            {"detail": "Cart item removed"}, status=status.HTTP_204_NO_CONTENT
        )
