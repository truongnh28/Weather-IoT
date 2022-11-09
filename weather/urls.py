from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add_weather'),
    path('delete/<city_name>/', views.delete, name='delete_city'),
]