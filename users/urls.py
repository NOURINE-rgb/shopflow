from django.urls import path

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
]
