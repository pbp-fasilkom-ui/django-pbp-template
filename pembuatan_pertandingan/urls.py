from django.urls import path
from pembuatan_pertandingan.views import *

app_name = 'pembuatan_pertandingan'

urlpatterns = [
    path('', show_page, name='show_page'),
    path('delete/<str:id_pertandingan>/',delete_pertandingan,name='delete_pertandingan'),
]