from django.urls import path
from pengelolaan.views import *

app_name = 'pengelolaan'

urlpatterns = [
    path('', tim, name='tim'),
    path('registrasi-tim/', registrasi_tim, name="registrasi_tim"),
    path('tambah-pemain/', tambah_pemain, name="tambah_pemain"),
    path('tambah-pelatih/', tambah_pelatih, name="tambah_pelatih"),
    path('make-captain/', make_captain, name="make_captain"),
    path('delete-pemain/', delete_pemain, name="delete_pemain"),
    path('delete-pelatih/', delete_pelatih, name="delete_pelatih"),
]