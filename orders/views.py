from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from orders.models import Order, OrderItem

from .serializers import CheckoutSerializer, OrderSerializer


# Create your views here.
class CheckoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data["address"]
        phone_number = serializer.validated_data["phone_number"]
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            total_price = 0
            order = Order.objects.create(
                user=request.user,
                total_price=0,
                address=address,
                phone_number=phone_number,
            )
            for item in cart.items.select_related("product"):
                product = item.product
                if item.quantity > product.stock:
                    transaction.set_rollback(True)
                    return Response(
                        {"error": f"Insufficient stock for product {product.name}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                product.stock -= item.quantity
                product.save()
                item_total = item.price * item.quantity
                total_price += item_total
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price,
                )
            order.total_price = total_price
            order.save()

            cart.items.all().delete()

        return Response(
            {
                "detail": "Order created successfully",
                "order_id": order.id,
            },
            status=status.HTTP_201_CREATED,
        )


class OrderListApiView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )


class OrderDetailApiView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )
