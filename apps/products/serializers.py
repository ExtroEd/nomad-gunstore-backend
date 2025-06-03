from rest_framework import serializers
from .models import Product
import random

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(children=None),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    price = serializers.IntegerField(
        required=True, min_value=0
    )
    discount_price = serializers.IntegerField(
        required=False, allow_null=True, min_value=0
    )
    has_free_shipping = serializers.SerializerMethodField()
    image = serializers.ImageField(
        required=False, default='img/Sample.jpg',
        allow_null=True, use_url=True
    )
    quantity = serializers.IntegerField(min_value=0, default=0)
    stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "category", "category_id",
            "price", "discount_price", "has_free_shipping", "image",
            "quantity", "stock", "sku", "mpn", "upc", "brand",
            "is_clearance", "is_deal_of_the_day", "created_at",
            "details", "features"
        ]
        read_only_fields = ["id", "created_at", "stock"]

    def get_has_free_shipping(self, obj) -> bool:
        return getattr(obj, "shipping_price", 0) == 0

    def validate(self, data):
        price = data.get('price')
        discount = data.get('discount_price')
        if discount is not None and price is not None and discount > price:
            raise serializers.ValidationError(
                "Цена со скидкой не может быть выше обычной цены."
            )
        return data

    def create(self, validated_data):
        if 'price' not in validated_data:
            validated_data['price'] = random.randint(100, 1_000_000)
        return super().create(validated_data)


class ProductCardSerializer(serializers.ModelSerializer):
    has_free_shipping = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "main_image", "price", "discount_price", "category",
            "is_deal_of_the_day", "is_clearance", "stock", "has_free_shipping"
        ]

    def get_main_image(self, obj):
        image = obj.get_main_image()
        if image and image.image:
            request = self.context.get('request')
            return request.build_absolute_uri(image.image.url) if request \
                else image.image.url
        return None

    def get_has_free_shipping(self, obj) -> bool:
        return getattr(obj, "shipping_price", 0) == 0
