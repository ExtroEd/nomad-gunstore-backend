from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart
from .serializers import CartSerializer


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return []  # Гостям разрешаем создание корзины
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)  # type: ignore
        elif (hasattr(self.request, 'session') and
              self.request.session.session_key):
            return Cart.objects.filter(  # type: ignore
                session_key=self.request.session.session_key
            )
        return Cart.objects.none()  # type: ignore

    def get_or_create_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(  # type: ignore
                user=request.user
            )
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(  # type: ignore
                session_key=session_key
            )
        return cart

    @extend_schema(
        summary="Список корзин",
        description="Получить корзину текущего пользователя. Только для "
                    "чтения.",
    )
    def list(self, request, *args, **kwargs):
        cart = self.get_or_create_cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @extend_schema(
        summary="Создание корзины",
        description="Создаёт новую корзину для авторизованного пользователя "
                    "или гостя. Только одна корзина на пользователя.",
        request=CartSerializer,
        responses=CartSerializer,
    )
    def create(self, request, *args, **kwargs):
        cart = self.get_or_create_cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=201)

    @extend_schema(
        summary="Получение корзины",
        description="Получает корзину текущего пользователя.",
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
        summary="Частичное обновление корзины",
        description="Позволяет изменить отдельные поля корзины без "
                    "необходимости передавать всё.",
        request=CartSerializer,
        responses=CartSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление корзины",
        description="Удаляет корзину. Доступно только для суперпользователей.",
    )
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'detail': 'Удаление корзины доступно только '
                           'суперпользователям.'},
                status=403
            )
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Текущая корзина",
        description="Возвращает корзину текущего пользователя или гостя по "
                    "session_key.",
        responses={200: CartSerializer}
    )
    @action(detail=False, methods=["get"], url_path="my")
    def my_cart(self, request):
        queryset = self.get_queryset()
        cart = queryset.first()

        if not cart:
            return Response({"detail": "Корзина не найдена."}, status=404)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)
