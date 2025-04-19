from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100
    )
    brand = models.CharField(
        max_length=255,
        blank=True
    )
    stock = models.BooleanField(
        default=True
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        default = 'img/Sample.jpg'
    )
    is_clearance = models.BooleanField(
        default=False
    )
    is_deal_of_the_day = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    attributes = models.JSONField(
        default=dict
    )
    details = RichTextField(blank=True)
    features = RichTextField(blank=True)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attribute_set'
    )
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"
