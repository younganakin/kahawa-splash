from django.urls import path

from . import views

app_name = 'kahawa'

urlpatterns = [
    path('', views.index, name='index'),
    path('verify', views.verify, name='verify'),
    path('welcome', views.welcome, name='welcome'),
]
