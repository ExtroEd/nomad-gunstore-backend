from rest_framework import generics, viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from drf_spectacular.utils import (extend_schema, OpenApiParameter,
                                   OpenApiExample)


@extend_schema(
    tags=["Products"],
    summary="List and create products",
    description="Получить список всех товаров или создать новый товар."
)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(
    tags=["Products"],
    summary="Retrieve, update or delete a product",
    description="Получить, обновить или удалить товар по ID."
)
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(
    tags=["Categories"],
    summary="List and create categories",
    description="Получить список всех категорий или создать новую категорию."
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
