from django.db import models


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logos/')
    site_name = models.CharField(max_length=100, default="Nomad Tactical")

    icon_search = models.FileField(upload_to='icons/', null=True, blank=True)
    icon_login = models.FileField(upload_to='icons/', null=True, blank=True)
    icon_help = models.FileField(upload_to='icons/', null=True, blank=True)
    icon_cart = models.FileField(upload_to='icons/', null=True, blank=True)

    def __str__(self):
        return self.site_name
