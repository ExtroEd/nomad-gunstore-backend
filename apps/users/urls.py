from django.urls import path
from .views import (RegisterView, LoginView, CustomTokenRefreshView,
                    UserListView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path("users/", UserListView.as_view(), name="user-list"),

]
