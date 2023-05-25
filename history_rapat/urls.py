from django.urls import path
from history_rapat.views import *

app_name = 'history_rapat'

urlpatterns = [
    path('', history_rapat, name='history_rapat'),
    path('isi_rapat/<uuid:id>',isi_rapat,name='isi_rapat')
]