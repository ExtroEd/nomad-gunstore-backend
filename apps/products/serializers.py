from rest_framework import serializers
from .models import Product
from apps.categories.models import Category
import random

from apps.categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    price = serializers.IntegerField(
        default=lambda: random.randint(100, 1_000_000)
    )
    discount_price = serializers.IntegerField(
        required=False, allow_null=True
    )
    has_free_shipping = serializers.SerializerMethodField()
    image = serializers.ImageField(
        required=False, default='img/Sample.jpg', allow_null=True,
        use_url=True
    )
    quantity = serializers.IntegerField(
        min_value=0, default=0
    )
    stock = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id", "category", "category_id", "price", "discount_price",
            "has_free_shipping", "image", "quantity", "stock", "name",
            "sku", "mpn", "upc", "brand", "is_clearance",
            "is_deal_of_the_day", "created_at", "details", "features"
        ]
        read_only_fields = ["id", "created_at", "stock"]

    def get_has_free_shipping(self, obj) -> bool:
        return obj.shipping_price == 0

    def validate(self, data):
        price = data.get('price')
        discount = data.get('discount_price')
        if discount is not None and price is not None and discount > price:
            raise serializers.ValidationError(
                "The discount price cannot be higher than the regular price."
            )
        return data

    def validate_category(self, value):
        if (value is not None and not Category.objects.filter(id=value.id).
                exists()):
            raise serializers.ValidationError("Категория не существует.")
        return value


class ProductCardSerializer(serializers.ModelSerializer):
    has_free_shipping = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "image", "price", "discount_price", "category",
            "is_deal_of_the_day", "is_clearance", "stock", "has_free_shipping"
        ]

    def get_has_free_shipping(self, obj) -> bool:
        return obj.shipping_price == 0
