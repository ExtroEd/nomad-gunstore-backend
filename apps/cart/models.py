from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
        blank=True, related_name="carts"
    )
    session_key = models.CharField(
        max_length=40, null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    shipping_protection = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Cart ({self.user or self.session_key})"

    @property
    def subtotal_price(self) -> int:
        return sum(
            item.total_price
            for item in self.items.all()  # type: ignore[attr-defined]
        )

    @property
    def shipping_fee(self) -> int:
        return sum(item.shipping_price
                   for item in self.items.all())  # type: ignore[attr-defined]

    @property
    def shipping_protection_fee(self) -> int:
        return int(self.subtotal_price * 0.03) \
            if self.shipping_protection else 0

    @property
    def final_price(self) -> int:
        return (self.subtotal_price + self.shipping_fee +
                self.shipping_protection_fee)


class CartItem(models.Model):
    cart = models.ForeignKey(
        'Cart', related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    @property
    def total_price(self):
        return self.product.price * self.quantity  # type: ignore[attr-defined]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def shipping_price(self):
        return (self.product.shipping_price *  # type: ignore[attr-defined]
                self.quantity)
