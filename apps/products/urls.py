from django.urls import path
from .views import (ProductListCreateView,
                    ProductRetrieveUpdateDestroyView,
                    CategoryListCreateView)


urlpatterns = [
    path('products/', ProductListCreateView.as_view(),
         name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(),
         name='product-detail'),
    path('categories/', CategoryListCreateView.as_view(),
         name='category-list-create'),
]
