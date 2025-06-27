from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.categories.models import Category, CustomMenuItem
from apps.categories.serializers import CategorySerializer, \
    RecursiveCategorySerializer, CustomMenuItemSerializer


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

    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.request.query_params.get('level')
        parent_id = self.request.query_params.get('parent')
        if level is not None:
            level = int(level)
            if level == 0:
                queryset = queryset.filter(parent__isnull=True)
            else:
                pass
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)
        return queryset


class MenuCategoryAPIView(APIView):
    serializer_class = RecursiveCategorySerializer

    def get(self, request):
        top_categories = Category.objects.filter(parent=None)
        serializer = self.serializer_class(top_categories, many=True)
        return Response(serializer.data)


class CustomMenuItemListView(generics.ListAPIView):
    queryset = CustomMenuItem.objects.prefetch_related("categories__children__children")
    serializer_class = CustomMenuItemSerializer
