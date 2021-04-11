from datas import views
from django.urls import path

urlpatterns = [
    path('data-raw/', views.DataRaw.as_view())
]