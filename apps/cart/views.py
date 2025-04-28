from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        elif hasattr(self.request,
                     'session') and self.request.session.session_key:
            return Cart.objects.filter(
                session_key=self.request.session.session_key)
        return Cart.objects.none()

    @extend_schema(
        summary="Список корзин",
        description="Получить корзину текущего пользователя. Только для "
                    "чтения.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание корзины",
        description="Создаёт новую корзину для авторизованного пользователя "
                    "или гостя. Только одна корзина на пользователя.",
        request=CartSerializer,
        responses=CartSerializer,
    )
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if Cart.objects.filter(user=request.user).exists():
                return Response({'detail': 'У вас уже есть корзина.'},
                                status=400)
        elif (
                not request.user.is_authenticated and 'session_key' not in
                request.data):
            return Response({
                                'detail': 'Для создания корзины необходимо '
                                          'указать session_key для гостей.'},
                            status=400)
        return super().create(request, *args, **kwargs)

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
                    "необходимости передавать всё. Например, можно обновить "
                    "только защиту доставки или сумму пожертвования.",
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
            return Response({
                                'detail': 'Удаление корзины доступно только '
                                          'суперпользователям.'},
                            status=403)

        return super().destroy(request, *args, **kwargs)
