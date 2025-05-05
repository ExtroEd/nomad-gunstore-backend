from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


def validate_zip(value):
    if not value.isdigit() or not value.startswith('72') or len(value) != 6:
        raise ValidationError(
            "Zip code must start with 72 and be 6 digits long"
        )


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=True
    )
    cart = models.OneToOneField(
        'cart.Cart', on_delete=models.CASCADE, related_name="order"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    state = models.CharField(max_length=50, choices=[
        ("Batken", "Batken"),
        ("Osh", "Osh"),
        ("Jalal-Abad", "Jalal-Abad"),
        ("Talas", "Talas"),
        ("Naryn", "Naryn"),
        ("Issyk-Kul", "Issyk-Kul"),
        ("Chui", "Chui"),
    ])
    zip_code = models.CharField(
        max_length=6, validators=[validate_zip]
    )
    giftcard_code = models.CharField(
        max_length=50, blank=True, null=True
    )
    discount_code = models.CharField(
        max_length=50, blank=True, null=True
    )
    is_paid = models.BooleanField(
        default=False
    )
    donation = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(99999)]
    )
    subtotal = models.PositiveIntegerField(
        default=0
    )
    shipping_fee = models.PositiveIntegerField(
        default=0
    )
    protection_fee = models.PositiveIntegerField(
        default=0
    )
    total = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"Order #{self.id}"

    def save(self, *args, **kwargs):
        self.subtotal = sum(item.quantity * item.product.price for item in
                            self.cart.items.all())
        self.shipping_fee = self.cart.shipping_fee or 0
        self.protection_fee = self.cart.shipping_protection_fee or 0
        self.total = (self.subtotal + self.shipping_fee + self.protection_fee +
                      self.donation)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
