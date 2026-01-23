from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Order, OrderItem


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Checkout Example",
            value={
                "address": "123 Main St, Springfield",
                "phone_number": "+213553866110",
            },
        )
    ]
)
class CheckoutSerializer(serializers.Serializer):
    address = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "total_price",
            "status",
            "address",
            "phone_number",
            "created_at",
            "items",
        ]


class UpdateStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.OrderStatus.choices)
