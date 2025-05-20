from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc (альтернатива Swagger)
    path('api/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.orders.urls')),
    path('api/', include('apps.carts.urls')),
    path('api/', include('apps.categories.urls')),

    # Frontend routes
    path('', include('apps.frontend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
