from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

def list_pertandingan_penonton(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'penonton':
            query1 = f'''select array_to_string(array_agg("nama_tim"),' VS ') as tim_bertanding, stadium.nama as nama_stadium, pertandingan.start_datetime as tanggal_dan_waktu, pertandingan.id_pertandingan
from pertandingan, tim_pertandingan, stadium
where tim_pertandingan.id_pertandingan = pertandingan.id_pertandingan and pertandingan.stadium = stadium.id_stadium
group by pertandingan.start_datetime, stadium.nama, pertandingan.id_pertandingan
order by pertandingan.start_datetime;
            '''
            cursor.execute(query1)
            list_pertandingan = cursor.fetchall()

            context = {
                'list_pertandingan': list_pertandingan,
                'role':'penonton',
            }
            return render(request, 'list_pertandingan.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
    
def list_pertandingan_manajer(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':
            query1 = '''select array_to_string(array_agg("nama_tim"),' VS ') as tim_bertanding, stadium.nama as nama_stadium, pertandingan.start_datetime as tanggal_dan_waktu
from pertandingan, tim_pertandingan, stadium
where tim_pertandingan.id_pertandingan = pertandingan.id_pertandingan and pertandingan.stadium = stadium.id_stadium
group by pertandingan.start_datetime, stadium.nama
order by pertandingan.start_datetime;

            '''
            cursor.execute(query1)
            list_pertandingan = cursor.fetchall()

            context = {
                'list_pertandingan': list_pertandingan,
                'role':'manajer',
            }
            return render(request, 'list_pertandingan.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
           
            
# Create your views here.
