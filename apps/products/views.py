import random

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (extend_schema_view, extend_schema,
                                   OpenApiParameter, OpenApiTypes)
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer, ProductCardSerializer
from apps.categories.models import Category


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
                description="Любой уровень категории (1–4)"
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
    description="Можно указать категорию любого уровня для фильтрации. "
                "Показываются товары с приоритетом Daily Deal, затем "
                "Clearance.",
    tags=["Products"],
    parameters=[
        OpenApiParameter(
            name='category', type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="ID любой категории. Включает подкатегории."
        )
    ],
    responses={200: ProductCardSerializer(many=True)}
)
class MainPageProductsAPIView(GenericAPIView):
    serializer_class = ProductCardSerializer
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request):
        category_id = request.query_params.get('category')
        product_filter = Q(stock=True)

        if category_id:
            try:
                category = Category.objects.get(
                    id=category_id
                )
                cat_ids = category.get_descendants(
                    include_self=True).values_list("id", flat=True
                                                   )
                product_filter &= Q(category_id__in=cat_ids)
            except Category.DoesNotExist:
                return Response({"detail": "Категория не найдена"},
                                status=404)

        def add_unique(products_queryset):
            nonlocal final_products, used_categories, used_product_ids
            products = list(products_queryset)
            random.shuffle(products)
            for product in products:
                if product.id in used_product_ids:
                    continue
                if (product.category_id not in used_categories or len(products)
                        <= 12):
                    final_products.append(product)
                    used_product_ids.add(product.id)
                    used_categories.add(product.category_id)
                if len(final_products) >= 12:
                    break

        final_products = []
        used_categories = set()
        used_product_ids = set()

        add_unique(Product.objects.filter(product_filter & Q(
            is_deal_of_the_day=True
        ))[:50])
        if len(final_products) < 12:
            add_unique(Product.objects.filter(product_filter & Q(
                is_clearance=True
            )))
        if len(final_products) < 12:
            add_unique(Product.objects.filter(product_filter))

        serializer = self.get_serializer(final_products[:12], many=True)
        return Response(serializer.data)


@extend_schema(
    summary="Получить все товары определённой категории",
    description="Возвращает все товары данной категории и её подкатегорий.",
    tags=["Products"],
    responses={200: ProductCardSerializer(many=True)}
)
class ProductsOfCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"detail": "Категория не найдена"},
                            status=status.HTTP_404_NOT_FOUND)

        descendant_ids = category.get_descendants(
            include_self=True
        ).values_list("id", flat=True)
        products = Product.objects.filter(
            category_id__in=descendant_ids, stock=True
        )
        serializer = ProductCardSerializer(
            products, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
