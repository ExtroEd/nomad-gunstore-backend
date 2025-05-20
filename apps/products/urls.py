from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, MainPageProductsAPIView, \
    ProductsOfCategoryAPIView

router = DefaultRouter()

router.register(r'products', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('main-page/', MainPageProductsAPIView.as_view(),
         name='main-page-products'),
    path("categories/<int:category_id>/products/",
         ProductsOfCategoryAPIView.as_view(), name="category-products"),
]
