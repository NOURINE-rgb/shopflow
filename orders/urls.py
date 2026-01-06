from django.urls import path

from .views import CheckoutApiView, OrderDetailApiView, OrderListApiView

urlpatterns = [
    path("checkout/", CheckoutApiView.as_view(), name="checkout"),
    path("", OrderListApiView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailApiView.as_view(), name="order-detail"),
]
