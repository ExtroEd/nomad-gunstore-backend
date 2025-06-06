from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, MainPageProductsAPIView, BrandListAPIView,
)


router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('main-page/', MainPageProductsAPIView.as_view(),
         name='main-page-products'),
    path('brands/', BrandListAPIView.as_view(), name='brands'),
]
