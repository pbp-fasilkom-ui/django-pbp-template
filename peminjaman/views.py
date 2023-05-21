from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


def peminjaman(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':
            id_manajer = request.COOKIES.get('uuid')
            query1 = f'''
            select s.nama, p.start_datetime, p.end_datetime, p.id_stadium from peminjaman p, stadium s where p.id_manajer = \'{id_manajer}\' and s.id_stadium = p.id_stadium ;
            '''
            cursor.execute(query1)
            peminjaman = cursor.fetchall()
            peminjaman_fix = []
            for i in peminjaman:
                temp = [i[0],i[1].strftime("%Y-%m-%d %H:%M:%S"),i[2].strftime("%Y-%m-%d %H:%M:%S"),i[3]]
                peminjaman_fix.append(temp)

            context = {
                'peminjaman': peminjaman_fix,
                'role':'manajer',
            }

            return render(request, 'peminjaman.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))

def buat_peminjaman(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':

            if request.method == "POST":

                tanggal_pinjam = request.POST.get('tanggal_pinjam')
                stadium = request.POST.get('stadium')

                cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '13 hour' as tanggal;")
                tanggal_waktu_mulai = cursor.fetchall()[0][0]

                cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '16 hour' as tanggal;")
                tanggal_waktu_akhir = cursor.fetchall()[0][0]

                manajer = request.COOKIES.get('uuid')

                try:
                    cursor.execute( f'''
                    INSERT INTO peminjaman (id_manajer, start_datetime, end_datetime, id_stadium) 
                    VALUES (\'{manajer}\', \'{tanggal_waktu_mulai}\', \'{tanggal_waktu_akhir}\', \'{stadium}\');
                    ''')
                    connection.commit()
                    return HttpResponseRedirect(reverse('peminjaman:peminjaman'))
                except Exception as e:
                    connection.rollback()
                    query1 = f'''
                    select nama, id_stadium from stadium;
                    '''
                    cursor.execute(query1)
                    stadium = cursor.fetchall()
                    context = {
                        'stadium': stadium,
                        'role':'manajer',
                        'message':'ERROR, stadium pada tanggal tersebut tidak tersedia'
                    }
                    return render(request, 'buat_peminjaman.html', context)

            query1 = f'''
            select nama, id_stadium from stadium;
            '''
            cursor.execute(query1)
            stadium = cursor.fetchall()


            context = {
                'stadium': stadium,
                'role':'manajer',
            }

            return render(request, 'buat_peminjaman.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))


def edit_peminjaman(request, tanggal):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':

            if request.method == "POST":

                tanggal_pinjam = tanggal

                stadium = request.POST.get('stadium')

                cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '0 hour' as tanggal;")
                tanggal_waktu_mulai = cursor.fetchall()[0][0]

                cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '3 hour' as tanggal;")
                tanggal_waktu_akhir = cursor.fetchall()[0][0]

                manajer = request.COOKIES.get('uuid')

                try:
                    cursor.execute( f'''
                    UPDATE peminjaman SET id_stadium = \'{stadium}\' 
                    WHERE id_manajer = \'{manajer}\' 
                    and start_datetime = \'{tanggal_waktu_mulai}\' 
                    and end_datetime =  \'{tanggal_waktu_akhir}\';
                    ''')
                    connection.commit()
                    return HttpResponseRedirect(reverse('peminjaman:peminjaman'))
                except Exception as e:
                    connection.rollback()
                    query1 = f'''
                    select nama, id_stadium from stadium;
                    '''
                    cursor.execute(query1)
                    stadium = cursor.fetchall()
                    context = {
                        'stadium': stadium,
                        'role':'manajer',
                        'message':'ERROR, stadium pada tanggal tersebut tidak tersedia'
                    }
                    return render(request, 'edit_peminjaman.html', context)

            query1 = f'''
            select nama, id_stadium from stadium;
            '''
            cursor.execute(query1)
            stadium = cursor.fetchall()


            context = {
                'stadium': stadium,
                'role':'manajer',
            }

            return render(request, 'edit_peminjaman.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))


