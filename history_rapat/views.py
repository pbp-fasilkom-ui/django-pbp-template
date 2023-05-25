from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt
    
def history_rapat(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':
            query1 = '''select array_to_string(array_agg("nama_tim"),' VS ') as rapat_tim, panitia.username as nama_panitia, stadium.nama as nama_stadium, pertandingan.start_datetime as tanggal_dan_waktu, rapat.id_pertandingan
from rapat, panitia, tim_pertandingan, stadium, pertandingan
where tim_pertandingan.id_pertandingan = rapat.id_pertandingan and pertandingan.id_pertandingan = rapat.id_pertandingan and pertandingan.stadium = stadium.id_stadium and rapat.perwakilan_panitia = panitia.id_panitia
group by pertandingan.start_datetime, stadium.nama, panitia.username, rapat.id_pertandingan
order by pertandingan.start_datetime;

            '''
            cursor.execute(query1)
            history_rapat = cursor.fetchall()

            context = {
                'history_rapat': history_rapat,
                'role':'manajer',
            }
            return render(request, 'history_rapat.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
           
def isi_rapat(request,id):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':

            query1 = f"select isi_rapat from rapat where id_pertandingan = \'{id}\'"
            cursor.execute(query1)
            isi_rapat = cursor.fetchall()

            context = {
                'isi_rapat' : isi_rapat,
                'role':'manajer',
            }

            return render(request, 'isi_rapat.html', context)

        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
# Create your views here.
# Create your views here.
