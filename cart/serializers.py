from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Add To Cart Example",
            value={"product_id": 1, "quantity": 2},
        )
    ]
)
class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Update Cart Item Example",
            value={"cart_item_id": 1, "quantity": 3},
        )
    ]
)
class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    cart_item_id = serializers.IntegerField()
