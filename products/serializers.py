from rest_framework import serializers
from .models import Product,Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
class ProductSerializer(serializers.ModelSerializer):
    is_discounted = serializers.ReadOnlyField()
    category = CategorySerializer(read_only=True)
    image = serializers.ImageField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock', 'is_hot', 'is_limited', 'discounted_price']