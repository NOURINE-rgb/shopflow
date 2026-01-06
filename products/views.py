from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(stock__gt=0)


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
