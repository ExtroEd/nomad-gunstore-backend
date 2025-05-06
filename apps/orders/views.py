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
        request=OrderSerializer,
        responses=OrderSerializer,
    )
    def create(self, request, *args, **kwargs):
        self.permission_classes = [AllowAny]
        self.check_permissions(request)

        cart_id = request.data.get("carts")
        if not cart_id:
            return Response({"detail": "Cart ID is required."},
                            status=400)

        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=404)

        if request.user.is_authenticated:
            if cart.user != request.user:
                return Response(
                    {"detail": "This carts does not belong to you."},
                    status=403)
        else:
            if cart.user is not None:
                return Response({"detail": "Unauthorized carts access."},
                                status=403)

        data = request.data.copy()
        if request.user.is_authenticated:
            data["user"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
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
