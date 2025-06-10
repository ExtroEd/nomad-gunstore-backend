from django.urls import path
from .views import SiteSettingsAPI


urlpatterns = [
    path('api/site-settings/', SiteSettingsAPI.as_view(),
         name='site-settings'),
]
