from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Name'
    )
    slug = models.SlugField(
        unique=True, blank=True
    )
    image = models.ImageField(
        upload_to='category_images/', null=True, blank=True
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE,
        verbose_name='Parent category'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug or self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_full_path(self):
        ancestors = []
        current = self
        while current:
            ancestors.append(current.name)
            current = current.parent
        return " > ".join(reversed(ancestors))


class CustomMenuItem(models.Model):
    MENU_CHOICES = [
        ("shop_all", "Shop All"),
        ("guns", "Guns"),
        ("ar_15", "AR-15"),
        ("ar_10", "AR-10"),
        ("ak_47", "AK-47"),
        ("ammo", "Ammo"),
        ("suppressors", "Suppressors"),
        ("brands", "Brands"),
    ]
    name = models.CharField(max_length=50, choices=MENU_CHOICES, unique=True)
    categories = models.ManyToManyField("Category", related_name="custom_menus")

    def __str__(self):
        return self.get_name_display()
