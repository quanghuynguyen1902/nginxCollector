from client import views
from django.urls import path

urlpatterns = [
    path('requests-data/', views.Requests.as_view()),
    path('requests-data/filter/', views.filter),
    path('requests-data/users/', views.get_users),
    path('requests-data/request-analytic/', views.request_method_analytic),
    path('requests-data/user-detail/', views.user_detail)
]