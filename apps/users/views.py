from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from apps.users.models import CustomUser
from apps.users.serializers import CustomUserSerializer
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


@extend_schema(
    tags=["Authentication"],
    summary="Получение списка всех пользователей",
    description="Эндпоинт для получения списка всех зарегистрированных "
                "пользователей системы. Доступен только администраторам.",
    responses={
        200: OpenApiResponse(
            description="Успешное выполнение. Возвращает список всех "
                        "пользователей.",
            response=CustomUserSerializer(many=True),
        ),
        403: OpenApiResponse(
            description="Ошибка доступа. Доступ разрешён только "
                        "администраторам.",
        ),
        500: OpenApiResponse(
            description="Ошибка сервера. Произошла непредвиденная ошибка.",
        ),
    },
)
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]
