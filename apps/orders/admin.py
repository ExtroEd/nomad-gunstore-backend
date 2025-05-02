from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'state', 'zip_code', 'is_paid', 'created_at', 'total'
    )
    list_filter = (
        'state', 'is_paid', 'created_at'
    )
    search_fields = (
        'user__username', 'zip_code', 'id'
    )
    readonly_fields = (
        'subtotal', 'shipping_fee', 'protection_fee', 'total'
    )
    inlines = [OrderItemInline]

    fieldsets = (
        ('User and Location', {
            'fields': ('user', 'state', 'zip_code')
        }),
        ('Codes and Payment', {
            'fields': ('giftcard_code', 'discount_code', 'is_paid')
        }),
        ('Price Info', {
            'fields': ('subtotal', 'shipping_fee', 'protection_fee', 'total')
        }),
        ('Cart', {
            'fields': ('cart',)
        }),
    )
