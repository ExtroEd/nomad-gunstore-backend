from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from drf_spectacular.utils import extend_schema

from .models import CustomUser
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Регистрация пользователя",
    description="Регистрация нового пользователя. "
                "Возвращает созданного пользователя.",
    responses={201: RegisterSerializer}
)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Authentication"],
    summary="Вход (получение токенов)",
    description="Аутентификация пользователя и получение JWT токена. "
                "Возвращает access и refresh токены, а также данные "
                "пользователя.",
)
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Authentication"],
    summary="Обновление access токена",
    description="Получение нового access токена по действующему refresh "
                "токену.",
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
