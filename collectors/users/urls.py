from users import views
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('user-by-app-key/', views.UserViewByAppKey.as_view())
]