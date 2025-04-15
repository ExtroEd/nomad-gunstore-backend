from django.contrib import admin
from .models import CustomUser  # Заменить на свою модель пользователя

admin.site.register(CustomUser)
