import django_filters
from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.NumberFilter(method="filter_by_category_tree")

    class Meta:
        model = Product
        fields = ["price_min", "price_max", "category"]

    def filter_by_category_tree(self, queryset, name, value):
        from apps.categories.models import Category

        try:
            category = Category.objects.get(id=value)
        except Category.DoesNotExist:
            return queryset.none()

        # Получаем id всех потомков, включая выбранную категорию
        category_ids = category.get_descendants(include_self=True).values_list("id", flat=True)
        return queryset.filter(category_id__in=category_ids)
