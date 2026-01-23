from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
@extend_schema(tags=["Products"])
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(stock__gt=0)


@extend_schema(tags=["Products"])
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
