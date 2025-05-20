from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=255
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
