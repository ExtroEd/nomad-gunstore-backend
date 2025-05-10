from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer
from ..products.models import Product


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        guest_allowed = [
            'create', 'add_item', 'remove_item',
            'clear_cart', 'update_item_quantity', 'my_cart'
        ]

        admin_only = ['list', 'retrieve']

        if self.action in guest_allowed:
            return []

        if self.action in admin_only:
            return [permissions.IsAdminUser()]

        return [
            permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.is_staff:
            return Cart.objects.all().order_by('id')

        if user.is_authenticated:
            return Cart.objects.filter(user=user).order_by('id')

        if hasattr(self.request,
                   'session') and self.request.session.session_key:
            return Cart.objects.filter(
                session_key=self.request.session.session_key
            ).order_by('id')

        return Cart.objects.none()

    def get_or_create_cart(self, request):
        user = request.user
        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
        elif hasattr(request, 'session') and request.session.session_key:
            cart, _ = Cart.objects.get_or_create(
                session_key=request.session.session_key)
        else:
            return None
        return cart

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.get(pk=self.kwargs["pk"])
        except Cart.DoesNotExist:
            raise NotFound("Корзина не найдена или доступ к ней запрещён.")

    @extend_schema(
        summary="Список корзин",
        description="Получить все корзины текущего пользователя (для отладки "
                    "или админов)."
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
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
        responses=CartSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()

        if request.user.is_superuser:
            return super().retrieve(request, *args, **kwargs)

        if request.user.is_authenticated:
            if cart.user != request.user:
                return Response({"detail": "Нет доступа к этой корзине."},
                                status=403)
        else:
            if cart.session_key != request.session.session_key:
                return Response({"detail": "Нет доступа к этой корзине."},
                                status=403)

        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление корзины",
        request=CartSerializer,
        responses=CartSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление корзины",
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
                {
                    'detail': 'Удаление корзины доступно только '
                              'суперпользователям.'},
                status=403
            )

        try:
            cart = Cart.objects.get(pk=kwargs['pk'])
        except Cart.DoesNotExist:
            return Response({'detail': 'Корзина не найдена.'}, status=404)

        cart.delete()
        return Response(status=204)

    @extend_schema(
        summary="Текущая корзина",
        description="Возвращает корзину текущего пользователя или гостя.",
        responses={200: CartSerializer}
    )
    @action(detail=False, methods=["get"], url_path="my")
    def my_cart(self, request):
        user = request.user

        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
        elif hasattr(request, 'session') and request.session.session_key:
            cart, _ = Cart.objects.get_or_create(
                session_key=request.session.session_key
            )
        else:
            return Response({"detail": "Невозможно определить сессию."},
                            status=400)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @extend_schema(
        summary="Добавление товара в корзину",
        description="Добавляет товар в корзину. Если товар уже есть — "
                    "увеличивает количество.",
        request={
            "application/json": {
                "example": {
                    "product": 1,
                    "quantity": 2
                }
            }
        },
        responses={200: {"type": "object", "properties": {
            "detail": {"type": "string"}
        }}},
    )
    @action(detail=False, methods=["post"], url_path="add-item")
    def add_item(self, request):
        cart = self.get_or_create_cart(request)
        if not cart:
            return Response({"detail": "Невозможно определить сессию."},
                            status=400)

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"detail": "Поле 'product' обязательно."},
                            status=400)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Товар не найден."}, status=404)

        item, created = CartItem.objects.get_or_create(cart=cart,
                                                       product=product)

        new_quantity = item.quantity + quantity if not created else quantity
        if new_quantity > product.quantity:
            return Response(
                {
                    "detail": f"Нельзя добавить {new_quantity} шт. — в "
                              f"наличии только {product.quantity}."},
                status=400
            )

        item.quantity = new_quantity
        item.save()
        return Response({"detail": "Товар добавлен в корзину."})

    @extend_schema(
        summary="Удалить товар из корзины",
        description="Удаляет указанный товар из корзины.",
        request={
            "application/json": {
                "example": {
                    "product": 1
                }
            }
        },
        responses={200: {"type": "object",
                         "properties": {"detail": {"type": "string"}}}},
    )
    @action(detail=False, methods=["post"], url_path="remove-item")
    def remove_item(self, request):
        cart = self.get_or_create_cart(request)
        if not cart:
            return Response({"detail": "Невозможно определить сессию."},
                            status=400)

        product_id = request.data.get("product")
        if not product_id:
            return Response({"detail": "Поле 'product' обязательно."},
                            status=400)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({"detail": "Товар удалён из корзины."})
        except CartItem.DoesNotExist:
            return Response({"detail": "Товар в корзине не найден."},
                            status=404)

    @extend_schema(
        summary="Очистить корзину",
        description="Удаляет все товары из корзины.",
        responses={200: {"type": "object",
                         "properties": {"detail": {"type": "string"}}}},
    )
    @action(detail=False, methods=["post"], url_path="clear")
    def clear_cart(self, request):
        cart = self.get_or_create_cart(request)
        if not cart:
            return Response({"detail": "Невозможно определить сессию."},
                            status=400)

        CartItem.objects.filter(cart=cart).delete()
        return Response({"detail": "Корзина очищена."})

    @extend_schema(
        summary="Обновить количество товара в корзине",
        description="Устанавливает новое количество указанного товара в "
                    "корзине.",
        request={
            "application/json": {
                "example": {
                    "product": 1,
                    "quantity": 3
                }
            }
        },
        responses={200: {"type": "object",
                         "properties": {"detail": {"type": "string"}}}},
    )
    @action(detail=False, methods=["post"], url_path="update-item")
    def update_item_quantity(self, request):
        cart = self.get_or_create_cart(request)
        if not cart:
            return Response({"detail": "Невозможно определить сессию."},
                            status=400)

        product_id = request.data.get("product")
        quantity = request.data.get("quantity")

        if not product_id or quantity is None:
            return Response(
                {"detail": "Поля 'product' и 'quantity' обязательны."},
                status=400)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Товар в корзине не найден."},
                            status=404)

        quantity = int(quantity)
        if quantity <= 0:
            item.delete()
            return Response(
                {"detail": "Товар удалён, так как количество стало 0."})

        if quantity > item.product.quantity:
            return Response(
                {
                    "detail": f"Нельзя установить {quantity} шт. — в наличии "
                              f"только {item.product.quantity}."},
                status=400
            )

        item.quantity = quantity
        item.save()
        return Response({"detail": "Количество обновлено."})
