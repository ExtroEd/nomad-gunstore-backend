from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Название'
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
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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
