from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CurrentUserApiView,
    EmailLoginApiView,
    ForgotPasswordApiView,
    RegisterApiView,
    ResetPasswordApiView,
)

urlpatterns = [
    path("register/", RegisterApiView.as_view()),
    path("login/", EmailLoginApiView.as_view()),
    path("me/", CurrentUserApiView.as_view()),
    path("forgot-password/", ForgotPasswordApiView.as_view()),
    path("reset-password/", ResetPasswordApiView.as_view()),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
