from django.urls import path

from . import views

app_name = 'vouchers'

urlpatterns = [
    path('', views.index, name='index'),
    path('download-vouchers',
         views.download_vouchers,
         name='download-vouchers'),
    path('generate-codes',
         views.generate_codes,
         name='generate-codes'),
]
