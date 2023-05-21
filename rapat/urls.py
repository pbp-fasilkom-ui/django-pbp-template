from django.urls import path
from rapat.views import *

app_name = 'rapat'

urlpatterns = [
    path('', rapat, name='rapat'),
    path('buat/<uuid:id>/<str:vs>',buat_rapat,name='buat_rapat'),
]