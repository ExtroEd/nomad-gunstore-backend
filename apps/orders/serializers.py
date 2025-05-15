from rest_framework import serializers
from .models import Order, OrderItem
from ..carts.models import Cart
from drf_spectacular.utils import extend_schema_field


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name"
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "total_price"]

    def get_total_price(self, obj) -> int:
        return obj.total_price


class OrderCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "session_key", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True, read_only=True
    )
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), required=True
    )
    subtotal = serializers.IntegerField(
        read_only=True
    )
    shipping_fee = serializers.IntegerField(
        read_only=True
    )
    protection_fee = serializers.IntegerField(
        read_only=True
    )
    total = serializers.IntegerField(
        read_only=True
    )
    donation = serializers.IntegerField(
        default=0, min_value=0, max_value=99999, required=False
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'user', 'created_at', 'subtotal', 'shipping_fee', 'protection_fee',
            'total'
        )

    def create(self, validated_data):
        user = self.context["request"].user
        cart = validated_data["cart"]

        if user.is_authenticated:
            validated_data["user"] = user

        errors = []
        for cart_item in cart.items.select_related('product'):
            product = cart_item.product
            if cart_item.quantity > product.stock:
                errors.append(
                    f"Товара '{product.name}' недостаточно, осталось "
                    f"{product.quantity} шт."
                )
        if errors:
            raise serializers.ValidationError({"detail": errors})

        donation = validated_data.get("donation", 0)

        validated_data["subtotal"] = cart.subtotal_price
        validated_data["shipping_fee"] = cart.shipping_fee
        validated_data["protection_fee"] = cart.shipping_protection_fee
        validated_data["total"] = (
                cart.subtotal_price + cart.shipping_fee +
                cart.shipping_protection_fee + donation
        )
        validated_data["donation"] = donation

        order = super().create(validated_data)

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()

        return order
