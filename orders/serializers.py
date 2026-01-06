from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):
    address = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)
