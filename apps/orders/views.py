from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Order
from .permissions import AllowCreateOrReadOnly
from .serializers import OrderSerializer
from ..carts.models import Cart


@extend_schema(tags=["Order"])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowCreateOrReadOnly]

    def get_or_create_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key,
                                                 user=None)
        return cart

    @extend_schema(
        summary="Список заказов",
        description="Получить список всех заказов. Может быть ограничено "
                    "правами пользователя.",
    )
    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание заказа",
        description="Создаёт новый заказ для пользователя или гостя, "
                    "привязывая корзину.",
        request={
            "application/json": {
                "example": {
                    "state": "Chui",
                    "zip_code": "720340",
                    "donation": 0,
                    "is_paid": True
                }
            }
        },
        responses=OrderSerializer,
    )
    def create(self, request, *args, **kwargs):
        self.permission_classes = [AllowAny]
        self.check_permissions(request)

        cart = self.get_or_create_cart(request)

        if request.user.is_authenticated:
            if cart.user != request.user:
                return Response(
                    {"detail": "This cart does not belong to you."},
                    status=403)
        else:
            if cart.user is not None:
                return Response({"detail": "Unauthorized cart access."},
                                status=403)

        data = request.data.copy()
        data["cart"] = cart.id
        if request.user.is_authenticated:
            data["user"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        cart.items.all().delete()
        return Response(serializer.data, status=201)

    @extend_schema(
        summary="Получение заказа",
        description="Получает заказ по ID, включая все товары и расчёты.",
        responses=OrderSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление заказа",
        description="Обновление информации о заказе, например, данных для "
                    "доставки.",
        request=OrderSerializer,
        responses=OrderSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление заказа",
        description="Позволяет обновить только часть информации о заказе.",
        request=OrderSerializer,
        responses=OrderSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление заказа",
        description="Удаляет заказ по ID.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
