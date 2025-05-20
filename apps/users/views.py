import random
import string

from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiResponse, \
    inline_serializer
from rest_framework import generics, permissions, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from apps.users.models import CustomUser
from apps.users.serializers import CustomUserSerializer, \
    EmailVerificationSerializer
from .serializers import (RegisterSerializer, CustomTokenObtainPairSerializer,
                          ResendVerificationCodeSerializer)
from .tasks import send_verification_email


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


@extend_schema(
    tags=["Authentication"],
    summary="Подтверждение email кода",
    description="Пользователь вводит код, полученный на почту, и подтверждает email.",
    request=EmailVerificationSerializer,
    responses={
        200: inline_serializer(
            name="EmailVerificationSuccessResponse",
            fields={
                "message": serializers.CharField(default="Email подтверждён!")
            }
        ),
        400: inline_serializer(
            name="EmailVerificationErrorResponse",
            fields={
                "email": serializers.ListField(
                    child=serializers.CharField(), required=False
                ),
                "code": serializers.ListField(
                    child=serializers.CharField(), required=False
                ),
            },
        ),
    }
)
class EmailVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Email подтверждён!"}, status=200)


class ResendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Повторная отправка кода подтверждения на email",
        description="Позволяет пользователю запросить повторную отправку "
                    "кода подтверждения. Реализована защита от спама.",
        tags=["Authentication"],
        request=ResendVerificationCodeSerializer,
        responses={
            200: OpenApiResponse(
                description="Код подтверждения повторно отправлен",
                response=ResendVerificationCodeSerializer
            ),
            400: OpenApiResponse(
                description="Неверные данные или попытка спама"
            ),
        }
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {"email": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cooldown_key = f"resend_cooldown_{email}"
        if cache.get(cooldown_key):
            return Response(
                {
                    "detail": "Пожалуйста, подождите минуту перед повторной "
                              "отправкой."
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    "detail": "Код отправлен, если такой email "
                              "зарегистрирован."
                },
                status=status.HTTP_200_OK
            )

        new_code = ''.join(random.choices(string.digits, k=6))
        user.verification_code = new_code
        user.save()

        send_verification_email.delay(email, new_code)

        cache.set(cooldown_key, True, timeout=60)

        return Response(
            {"detail": "Код подтверждения отправлен повторно."},
            status=status.HTTP_200_OK
        )
