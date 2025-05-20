from drf_spectacular.utils import (extend_schema_view, extend_schema)
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer


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
