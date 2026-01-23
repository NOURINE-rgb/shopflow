from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    EmailLoginSerializer,
    ForgotPasswordSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)


# Create your views here.
@extend_schema(tags=["Authentication"], request=RegisterSerializer, responses=201)
class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "detail": "User registered successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Authentication"], request=EmailLoginSerializer, responses=200)
class EmailLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "detail": "Login successful",
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Authentication"],
    responses=200,
)
class CurrentUserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Authentication"])
class ForgotPasswordApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "If the email is registered, a reset link has been sent."},
                status=status.HTTP_200_OK,
            )
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://example.com/reset-password/?uid={uidb64}&token={token}"
        return Response(
            {"detail": "If the email is registered, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication"])
class ResetPasswordApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]
        uid = request.data.get("uid")

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response({"detail": "Invalid token"}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"detail": "Invalid token"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password reset successful"})
