from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ProductSerializer(serializers.ModelSerializer):
    is_discounted = serializers.ReadOnlyField()
    category = CategorySerializer(read_only=True)

    @extend_schema_field(serializers.URLField())
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "image",
            "price",
            "is_discounted",
            "is_hot",
            "is_limited",
            "discounted_price",
            "stock",
        ]
