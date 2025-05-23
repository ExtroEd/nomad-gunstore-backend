from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
                request.user and request.user.is_staff
        )


@extend_schema_view(
    list=extend_schema(summary="Список всех категорий"),
    create=extend_schema(summary="Создание категории"),
    retrieve=extend_schema(summary="Получение категории"),
    update=extend_schema(summary="Обновление категории"),
    partial_update=extend_schema(summary="Частичное обновление категории"),
    destroy=extend_schema(summary="Удаление категории"),
)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    # Дополнительно можно сделать фильтрацию по уровню или по родителю,
    # чтобы можно было получить, например, только категории 0 уровня
    # (parent=None)
    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.request.query_params.get('level')
        parent_id = self.request.query_params.get('parent')
        if level is not None:
            level = int(level)
            # Фильтрация по уровню: уровень 0 — parent = None,
            # уровень 1 — parent у которого parent=None и т.д.
            # Реализовать это можно рекурсивно, либо через аннотацию, но проще:
            if level == 0:
                queryset = queryset.filter(parent__isnull=True)
            else:
                # Для упрощения можно фильтровать по parent на основе ID,
                # или добавить поле depth в модель (по желанию).
                pass  # Можно доработать, если надо
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)
        return queryset
