from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CheckoutSerializer


# Create your views here.
class CheckoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data["address"]
        phone_number = serializer.validated_data["phone_number"]
        # Here you would typically create an order, process payment, etc.
        return Response(
            {
                "detail": "Checkout successful",
                "address": address,
                "phone_number": phone_number,
            },
            status=status.HTTP_200_OK,
        )
