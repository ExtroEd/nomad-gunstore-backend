from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    MainPageProductsAPIView,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('main-page/', MainPageProductsAPIView.as_view(),
         name='main-page-products'),
]
