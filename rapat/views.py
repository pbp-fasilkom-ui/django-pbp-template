from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

def rapat(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':
            query1 = '''
            SELECT STRING_AGG(TP.nama_tim,' vs ') AS tim_tanding, 
            S.nama, P.start_datetime, P.end_datetime, 
            P.id_pertandingan FROM Pertandingan P, Tim_Pertandingan TP, stadium S 
            WHERE TP.id_pertandingan = P.id_pertandingan AND S.id_stadium = P.stadium
            AND P.id_pertandingan 
            NOT IN (SELECT rapat.id_pertandingan FROM rapat) GROUP BY P.id_pertandingan, S.nama;
            '''
            cursor.execute(query1)
            rapat = cursor.fetchall()

            context = {
                'rapat': rapat,
                'role':'panitia',
            }
            return render(request, 'rapat.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))

def buat_rapat(request,id,vs):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':

            context = {
                'vs': vs,
                'role':'panitia',
            }

            if request.method == "POST":
                duatim = vs.split(" vs ")
                tim1 = duatim[0]
                tim2 = duatim[1]

                cursor.execute(f"select id_manajer from tim_manajer where nama_tim = \'{tim1}\' ")
                manajertim1 = cursor.fetchmany()[0][0]

                cursor.execute(f"select id_manajer from tim_manajer where nama_tim = \'{tim2}\' ")
                manajertim2 = cursor.fetchmany()[0][0]

                cursor.execute(f"select (start_datetime - interval '10 days') from pertandingan where id_pertandingan = \'{id}\'")
                getdate = cursor.fetchmany()[0][0]

                cursor.execute(f"select p.id_panitia from panitia p where p.id_panitia not in (select rapat.perwakilan_panitia from rapat where (manajer_tim_a = \'{manajertim1}\' and manajer_tim_b = \'{manajertim2}\') or (manajer_tim_a = \'{manajertim2}\' and manajer_tim_b = \'{manajertim1}\') );")
                idpanitia = cursor.fetchmany()[0][0]
                
                text = request.POST.get('isi')

                cursor.execute(
                f'''INSERT INTO Rapat (ID_Pertandingan, Datetime, Perwakilan_Panitia, Manajer_Tim_A, Manajer_Tim_B, Isi_Rapat) 
                VALUES (\'{id}\', \'{getdate}\', \'{idpanitia}\', \'{manajertim1}\', \'{manajertim2}\', \'{text}\');'''
                )
                connection.commit()

                return HttpResponseRedirect(reverse('example_app:dashboard'))

            return render(request, 'buat_rapat.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
