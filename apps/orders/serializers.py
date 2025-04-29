from rest_framework import serializers
from .models import Order, OrderItem
from ..cart.models import Cart
from drf_spectacular.utils import extend_schema_field


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "total_price"]

    def get_total_price(self, obj) -> int:
        return obj.total_price


class OrderCartSerializer(serializers.ModelSerializer):
    # Пример простого сериализатора для корзины, если необходимо передавать
    # корзину в заказе. Вы можете расширить его под вашу логику
    class Meta:
        model = Cart
        fields = ["id", "session_key", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(),
        required=True
    )

    subtotal = serializers.SerializerMethodField()
    shipping_fee = serializers.SerializerMethodField()
    protection_fee = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id", "user", "cart", "created_at", "state", "zip_code",
            "giftcard_code", "discount_code", "is_paid", "items",
            "subtotal", "shipping_fee", "protection_fee", "total"
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    @staticmethod
    def _get_integer_field(obj, field_name):
        value = getattr(obj, field_name, 0)
        return int(value) if value is not None else 0

    @extend_schema_field(serializers.IntegerField())
    def get_subtotal(self, obj):
        return self._get_integer_field(obj, "subtotal")

    @extend_schema_field(serializers.IntegerField())
    def get_shipping_fee(self, obj):
        return self._get_integer_field(obj, "shipping_fee")

    @extend_schema_field(serializers.IntegerField())
    def get_protection_fee(self, obj):
        return self._get_integer_field(obj, "protection_fee")

    @extend_schema_field(serializers.IntegerField())
    def get_total(self, obj):
        return self._get_integer_field(obj, "total")
