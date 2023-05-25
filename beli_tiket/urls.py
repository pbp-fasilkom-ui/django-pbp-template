from django.urls import path
from beli_tiket.views import *

app_name = 'beli_tiket'

urlpatterns = [
    path('', list_pertandingan_tiket, name='list_pertandingan_tiket'),
    path('list_tiket/<str:id>', list_tiket, name='list_tiket'),
    path('beli_tiket/<str:id>', beli_tiket, name='beli_tiket'),
]