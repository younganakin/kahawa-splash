from django.urls import path

from . import views

app_name = 'java'

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome', views.welcome, name='welcome'),
]
