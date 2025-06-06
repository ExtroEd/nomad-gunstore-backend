from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.categories.views import CategoryViewSet, MenuCategoryAPIView


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('menu-categories/', MenuCategoryAPIView.as_view(),
         name='menu-categories'),
]
