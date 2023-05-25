from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
import random
import string
from django.views.decorators.csrf import csrf_exempt

def list_pertandingan_tiket(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'penonton':
            query1 = f'''select array_to_string(array_agg("nama_tim"),' VS ') as tim_bertanding, stadium.nama as nama_stadium, pertandingan.start_datetime as tanggal_dan_waktu, pertandingan.id_pertandingan as id_pertandingan
from pertandingan, tim_pertandingan, stadium
where tim_pertandingan.id_pertandingan = pertandingan.id_pertandingan and pertandingan.stadium = stadium.id_stadium
group by pertandingan.start_datetime, stadium.nama, pertandingan.id_pertandingan
order by pertandingan.start_datetime;

            '''
            cursor.execute(query1)
            list_pertandingan_tiket = cursor.fetchall()
            print(list_pertandingan_tiket)
            context = {
                'list_pertandingan_tiket': list_pertandingan_tiket,
                'role':'penonton',
            }
            return render(request, 'beli_tiket.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
    
def list_tiket(request,id):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'penonton':
            query1 = f'''select jenis_tiket from pembelian_tiket
            '''
            cursor.execute(query1)
            list_tiket = cursor.fetchall()

            query2 = f'''select jenis_pembayaran from pembelian_tiket'''
            cursor.execute(query2)
            list_pembayaran = cursor.fetchall()

            context = {
                'list_tiket': list_tiket,
                'list_pembayaran': list_pembayaran,
                'role':'penonton',
            }
            return render(request, 'pilih_tiket.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
    
def beli_tiket(request, jenis_tiket, jenis_pembayaran, id):
    jenis_tiket = request.POST.get('jenis_tiket')
    jenis_pembayaran = request.POST.get('jenis_pembayaran')
    id_penonton = request.COOKIES.get('uuid')
    nmr_receipt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))

    query1='''INSERT INTO "Pembelian_Tiket" (
                nomor_receipt, 
                id_penonton, 
                id_pertandingan, 
                jenis_tiket, 
                jenis_embayaran
            ) VALUES (\'{nmr_receipt}\', \'{id_penonton}\', \'{id_pertandingan}\', \'{jenis_tiket}\', \'{jenis_pembayaran}\')'''
    cursor.execute(query1)
    return render(request, 'beli_tiket.html')
