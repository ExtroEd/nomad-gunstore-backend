from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    @extend_schema_field(serializers.IntegerField())
    def get_total_price(self, obj):
        return obj.total_price

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total_price']
        read_only_fields = ['total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    @extend_schema_field(serializers.IntegerField())
    def get_subtotal_price(self, obj):
        return obj.subtotal_price

    @extend_schema_field(serializers.IntegerField())
    def get_shipping_fee(self, obj):
        return obj.shipping_fee

    @extend_schema_field(serializers.IntegerField())
    def get_shipping_protection_fee(self, obj):
        return obj.shipping_protection_fee

    @extend_schema_field(serializers.IntegerField())
    def get_final_price(self, obj):
        return obj.final_price

    subtotal_price = serializers.SerializerMethodField()
    shipping_fee = serializers.SerializerMethodField()
    shipping_protection_fee = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'session_key', 'created_at', 'items',
            'subtotal_price', 'shipping_fee', 'shipping_protection_fee',
            'final_price'
        ]
        read_only_fields = [
            'id', 'created_at', 'subtotal_price', 'shipping_fee',
            'shipping_protection_fee', 'final_price'
        ]
