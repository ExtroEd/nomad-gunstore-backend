from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    subtotal = serializers.ReadOnlyField()
    shipping_fee = serializers.ReadOnlyField()
    protection_fee = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            "id", "user", "cart", "created_at", "state", "zip_code",
            "giftcard_code", "discount_code", "is_paid", "items",
            "subtotal", "shipping_fee", "protection_fee", "total"
        ]

    def create(self, validated_data):
        # Если корзина не передана, а только ID, найдем её
        cart = validated_data.get("cart")
        if not cart:
            raise serializers.ValidationError("Cart must be provided")

        order = Order.objects.create(cart=cart, **validated_data)
        return order
