from rest_framework import serializers
from .models import Product, Category
import random


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    price = serializers.IntegerField(
        default=lambda: random.randint(1, 1_000_000)
    )
    discount_price = serializers.IntegerField(
        required=False, allow_null=True
    )
    image = serializers.ImageField(
        required=False, default='img/Sample.jpg'
    )

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        price = data.get('price')
        discount = data.get('discount_price')
        if discount is not None and price is not None and discount > price:
            raise serializers.ValidationError(
                "The discount price cannot be higher than the regular price."
            )
        return data
