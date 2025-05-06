from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ("product", "quantity")
    autocomplete_fields = ("product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "created_at", "updated_at")
    search_fields = ("user__username", "session_key")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [CartItemInline]
