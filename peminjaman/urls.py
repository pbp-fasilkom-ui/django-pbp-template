from django.urls import path
from peminjaman.views import *

app_name = 'peminjaman'

urlpatterns = [
    path('', peminjaman, name='peminjaman'),
    path('buat/', buat_peminjaman, name="buat_peminjaman"),
    path('edit/<str:tanggal>',edit_peminjaman,name='edit_peminjaman'),
]