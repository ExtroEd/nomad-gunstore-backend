import random

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (extend_schema_view, extend_schema,
                                   OpenApiParameter, OpenApiTypes)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import Category, Product
from .serializers import (ProductSerializer, CategorySerializer,
                          ProductMainPageSerializer)
from django.core.cache import cache



class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает безопасные методы всем (GET, HEAD, OPTIONS),
    а все остальные — только админам.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


@extend_schema_view(
    list=extend_schema(
        summary="Список категорий",
        description="Возвращает все доступные категории. Поддерживает "
                    "вложенные категории.",
        tags=["Categories"]
    ),
    create=extend_schema(
        summary="Создание категории",
        description="Создаёт новую категорию. Можно указать родительскую "
                    "категорию через `parent`.",
        tags=["Categories"]
    ),
    retrieve=extend_schema(
        summary="Получение категории",
        description="Возвращает одну категорию по ID.",
        tags=["Categories"]
    ),
    update=extend_schema(
        summary="Обновление категории",
        description="Полное обновление категории.",
        tags=["Categories"]
    ),
    partial_update=extend_schema(
        summary="Частичное обновление категории",
        description="Обновляет отдельные поля категории.",
        tags=["Categories"]
    ),
    destroy=extend_schema(
        summary="Удаление категории",
        description="Удаляет категорию по ID. Подкатегории могут остаться "
                    "без родителя.",
        tags=["Categories"]
    ),
)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('id')  # type: ignore[arg-type]
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="Список продуктов",
        description="Возвращает список всех продуктов. Поддерживает "
                    "фильтрацию и пагинацию.",
        tags=["Products"],
        parameters=[
            OpenApiParameter(
                name='search', type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,  # type: ignore[arg-type]
                description="Поиск по имени или описанию"
            ),
            OpenApiParameter(
                name="price_min", type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,  # type: ignore[arg-type]
                description="Минимальная цена"
            ),
            OpenApiParameter(
                name="price_max", type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,  # type: ignore[arg-type]
                description="Максимальная цена"
            ),
            OpenApiParameter(
                name='category', type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,  # type: ignore[arg-type]
                description="ID категории"
            ),
            OpenApiParameter(
                name='ordering', type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,  # type: ignore[arg-type]
                description="Сортировка по `price`, `-price`, `name` и т.д."
            ),
            OpenApiParameter(
                name='page', type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,  # type: ignore[arg-type]
                description="Номер страницы"),
        ]
    ),
    create=extend_schema(
        summary="Создание продукта",
        description="Создаёт новый продукт. Укажите все нужные поля, включая "
                    "категорию.",
        tags=["Products"]
    ),
    retrieve=extend_schema(
        summary="Получение продукта",
        description="Возвращает подробную информацию о продукте по его ID.",
        tags=["Products"]
    ),
    update=extend_schema(
        summary="Обновление продукта",
        description="Полное обновление продукта. Все поля обязательны.",
        tags=["Products"]
    ),
    partial_update=extend_schema(
        summary="Частичное обновление продукта",
        description="Обновление одного или нескольких полей продукта.",
        tags=["Products"]
    ),
    destroy=extend_schema(
        summary="Удаление продукта",
        description="Удаляет продукт по ID. Действие необратимо.",
        tags=["Products"]
    ),
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')  # type: ignore[arg-type]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['price']
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    summary="Главная страница: 12 товаров",
    description="Товары из разных категорий, в приоритете Daily Deal и "
                "Clearance.",
    tags=["Products"]
)
class MainPageProductsAPIView(GenericAPIView):
    serializer_class = ProductMainPageSerializer
    queryset = Product.objects.none()
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request):
        final_products = []
        used_categories = set()
        used_product_ids = set()

        def add_unique(products_queryset):
            nonlocal final_products, used_categories, used_product_ids
            products = list(products_queryset)
            random.shuffle(products)
            for product in products:
                if product.id in used_product_ids:
                    continue
                cat_id = product.category_id
                if cat_id not in used_categories or len(products) <= 12:
                    final_products.append(product)
                    used_product_ids.add(product.id)
                    used_categories.add(cat_id)
                if len(final_products) >= 12:
                    break

        add_unique(Product.objects.filter(is_deal_of_the_day=True, stock=True))

        if len(final_products) < 12:
            add_unique(Product.objects.filter(is_clearance=True, stock=True))

        if len(final_products) < 12:
            add_unique(Product.objects.filter(stock=True))

        serializer = self.get_serializer(final_products[:12], many=True)
        return Response(serializer.data)
