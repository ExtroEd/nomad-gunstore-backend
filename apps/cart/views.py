from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from .models import Cart
from .serializers import CartSerializer


@extend_schema(
    tags=["Cart"],
)
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()  # type: ignore[attr-defined]
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Список корзин",
        description="Получить список всех корзин. Только для чтения. Обычно "
                    "используется для отладки или админки.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание корзины",
        description="Создаёт новую корзину. Работает как для авторизованных "
                    "пользователей, так и для гостей по session_key.",
        request=CartSerializer,
        responses=CartSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение корзины",
        description="Получает корзину по её ID. Включает список товаров, "
                    "суммы и параметры доставки.",
        responses=CartSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление корзины",
        description="Обновляет параметры корзины — можно изменить защиту "
                    "доставки, пожертвование, почтовый код и т.д.",
        request=CartSerializer,
        responses=CartSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление корзины",
        description="Удаляет выбранную корзину по ID.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
