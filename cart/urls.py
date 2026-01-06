from django.urls import path

from .views import (
    AddToCartApiView,
    CartDetailApiView,
    RemoveCartItemApiView,
    UpdateCartItemApiView,
)

urlpatterns = [
    path("", CartDetailApiView.as_view(), name="cart-detail"),
    path("add/", AddToCartApiView.as_view(), name="add-to-cart"),
    path("update/", UpdateCartItemApiView.as_view(), name="update-cart-item"),
    path(
        "remove/<int:cart_item_id>/",
        RemoveCartItemApiView.as_view(),
        name="remove-cart-item",
    ),
]
