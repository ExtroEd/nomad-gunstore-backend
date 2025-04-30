from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


@extend_schema(tags=["Order"])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  #type: ignore
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Список заказов",
        description="Получить список всех заказов. Может быть ограничено "
                    "правами пользователя.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание заказа",
        description="Создаёт новый заказ для пользователя или гостя, "
                    "привязывая корзину.",
        request=OrderSerializer,
        responses=OrderSerializer,
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'orders_order_cart_id_key' in str(e):
                return Response(
                    {"detail": "Эта корзина уже была использована в заказе."},
                    status=status.HTTP_409_CONFLICT
                )
            return Response(
                {"detail": "Ошибка при создании заказа."},
                status=status.HTTP_400_BAD_REQUEST
            )

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
