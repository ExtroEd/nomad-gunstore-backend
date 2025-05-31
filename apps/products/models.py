import random
import string

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from apps.categories.models import Category


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    headline = models.CharField(
        max_length=255,
        blank=True,
    )
    logo = models.ImageField(upload_to='brands/logos/', null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug or self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("brands:detail", kwargs={"slug": self.slug})


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Category"
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    discount_price = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, null=True
    )
    shipping_price = models.PositiveIntegerField(
        default=2000
    )
    sku = models.CharField(
        max_length=19, unique=True, editable=False, blank=True, null=True
    )
    mpn = models.CharField(
        max_length=12, unique=True, editable=False, blank=True, null=True
    )
    upc = models.CharField(
        max_length=12, unique=True, editable=False, blank=True, null=True
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='products', null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        default=0
    )
    stock = models.BooleanField(
        default=False, editable=False
    )
    is_clearance = models.BooleanField(
        default=False
    )
    is_deal_of_the_day = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    details = CKEditor5Field(
        'Details',
        config_name='default',
        default="",
        blank=True,
        null=True
    )
    features = CKEditor5Field(
        'Features',
        config_name='default',
        default="",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.sku:
            now = timezone.now().strftime('%Y%m%d%H%M')
            rand = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=5)
            )
            self.sku = f"{now}-{rand}"

        if not self.mpn:
            self.mpn = ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits + '-',
                    k=random.randint(6, 12)
                )
            )

        if not self.upc:
            self.upc = ''.join(random.choices(string.digits, k=12))

        self.stock = self.quantity >= 1  # type: ignore

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_round_count(self):
        for attr in self.attribute_set.all():
            if attr.key.lower() == "round count":
                try:
                    return int(attr.value)
                except ValueError:
                    return None
        return None

    def get_price_per_round(self):
        round_count = self.get_round_count()
        if round_count and round_count > 0:
            return round(self.price / round_count, 2)
        return None

    def get_main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='products/images/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product,
                                        is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='attribute_set'
    )
    key = models.CharField(
        max_length=255
    )
    value = models.CharField(
        max_length=255
    )

    def save(self, *args, **kwargs):
        if self.key:
            self.key = self.key.strip().lower()
        if isinstance(self.value, str):
            self.value = self.value.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.key}: {self.value}"
