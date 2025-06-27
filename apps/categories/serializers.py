from typing import List

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.categories.models import Category, CustomMenuItem


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'parent']


class RecursiveCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'children']

    @extend_schema_field(lambda: RecursiveCategorySerializer(many=True))
    def get_children(self, obj) -> List[dict]:
        if obj.children.exists():
            return RecursiveCategorySerializer(
                obj.children.all(),
                many=True,
                context=self.context
            ).data
        return []


class CustomMenuItemSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = CustomMenuItem
        fields = ["name", "categories"]
