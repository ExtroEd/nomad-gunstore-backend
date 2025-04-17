from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import (extend_schema_view, extend_schema,
                                   OpenApiParameter, OpenApiTypes)
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter


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
    queryset = Category.objects.all()  # type: ignore[arg-type]
    serializer_class = CategorySerializer


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
    queryset = Product.objects.all()  # type: ignore[arg-type]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['price']
