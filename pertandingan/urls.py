from django.urls import path
from pertandingan.views import *

app_name = 'pertandingan'

urlpatterns = [
    path('', pertandingan, name='pertandingan'),
    path('mulai/<str:id_pertandingan>/', mulai_pertandingan, name="mulai_pertandingan"),
    path('peristiwa/<str:id_pertandingan>/<str:nama_tim>/', pilih_peristiwa, name="pilih_peristiwa"),    
]