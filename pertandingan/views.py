from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


def pertandingan(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':
            id_panitia = request.COOKIES.get('uuid')

            query_pertandingan = f"""
                SELECT ID_pertandingan, start_datetime 
                FROM PERTANDINGAN;
            """
            cursor.execute(query_pertandingan)
            daftar_pertandingan = cursor.fetchall()

            daftar_pertandingan_fix = []
            peristiwa_tim1_fix = []

            for pertandingan in daftar_pertandingan:
                UUID_pertandingan = pertandingan[0]

                datetime_pertandingan = pertandingan[1]
                status = ""
                countdown_mulai = (datetime_pertandingan -
                                   datetime.now()).total_seconds() / 60
                if countdown_mulai <= 5 and countdown_mulai > 0:
                    status = "berlangsung"
                elif countdown_mulai > 5:
                    status = "belum mulai"
                else:
                    status = "selesai"

                get_tim_pertandingan = f'''
                    SELECT skor, nama_tim
                    FROM TIM_PERTANDINGAN
                    WHERE ID_pertandingan =  \'{UUID_pertandingan}\';
                '''
                cursor.execute(get_tim_pertandingan)
                tim_pertandingan = cursor.fetchmany(2)
                nama_tim1 = tim_pertandingan[0][1]
                nama_tim2 = tim_pertandingan[1][1]
                skor_tim1 = tim_pertandingan[0][0]
                skor_tim2 = tim_pertandingan[1][0]

                get_peristiwa_tim1 = f'''
                    SELECT CONCAT(nama_depan, ' ', nama_belakang), jenis     
                    FROM PEMAIN NATURAL JOIN PERISTIWA
                    WHERE nama_tim = \'{nama_tim1}\' AND
                    ID_pertandingan = \'{UUID_pertandingan}\';
                '''

                cursor.execute(get_peristiwa_tim1)
                peristiwa_tim1 = cursor.fetchall()
                peristiwa_tim1_fix.append(peristiwa_tim1)

                get_peristiwa_tim2 = f'''
                    SELECT CONCAT(nama_depan, ' ', nama_belakang), jenis     
                    FROM PEMAIN NATURAL JOIN PERISTIWA
                    WHERE nama_tim = \'{nama_tim2}\' AND
                    ID_pertandingan = \'{UUID_pertandingan}\';
                '''

                cursor.execute(get_peristiwa_tim2)
                peristiwa_tim2 = cursor.fetchall()

                pemenang = nama_tim2
                if skor_tim1 > skor_tim2:
                    pemenang = nama_tim1

                pertandingan_fix = (
                    pertandingan[1], nama_tim1, nama_tim2, status, pemenang, peristiwa_tim1,peristiwa_tim2)
                daftar_pertandingan_fix.append(pertandingan_fix)


            context = {
                'daftar_pertandingan': daftar_pertandingan_fix,
                # 'pertandingan': daftar_pertandingan,
                'role': 'panitia',
                'test': peristiwa_tim1_fix
            }

            return render(request, 'mengelola_pertandingan.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))


def mulai_pertandingan(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':

            if request.method == "POST":

                tanggal_pinjam = request.POST.get('tanggal_pinjam')
                stadium = request.POST.get('stadium')

                cursor.execute(
                    f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '13 hour' as tanggal;")
                tanggal_waktu_mulai = cursor.fetchall()[0][0]

                cursor.execute(
                    f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '16 hour' as tanggal;")
                tanggal_waktu_akhir = cursor.fetchall()[0][0]

                panitia = request.COOKIES.get('uuid')

                try:
                    cursor.execute(f'''
                    INSERT INTO pertandingan (id_panitia, start_datetime, end_datetime, id_stadium) 
                    VALUES (\'{panitia}\', \'{tanggal_waktu_mulai}\', \'{tanggal_waktu_akhir}\', \'{stadium}\');
                    ''')
                    connection.commit()
                    return HttpResponseRedirect(reverse('pertandingan:pertandingan'))
                except Exception as e:
                    connection.rollback()
                    query1 = f'''
                    select nama, id_stadium from stadium;
                    '''
                    cursor.execute(query1)
                    stadium = cursor.fetchall()
                    context = {
                        'stadium': stadium,
                        'role': 'panitia',
                        'message': 'ERROR, stadium pada tanggal tersebut tidak tersedia'
                    }
                    return render(request, 'buat_pertandingan.html', context)

            query1 = f'''
            select nama, id_stadium from stadium;
            '''
            cursor.execute(query1)
            stadium = cursor.fetchall()

            context = {
                'stadium': stadium,
                'role': 'panitia',
            }

            return render(request, 'mulai_pertandingan.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))


def pilih_peristiwa(request, nama_tim):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':

            # if request.method == "POST":

            #     tanggal_pinjam = tanggal

            #     stadium = request.POST.get('stadium')

            #     cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '0 hour' as tanggal;")
            #     tanggal_waktu_mulai = cursor.fetchall()[0][0]

            #     cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '3 hour' as tanggal;")
            #     tanggal_waktu_akhir = cursor.fetchall()[0][0]

            #     panitia = request.COOKIES.get('uuid')

            #     try:
            #         cursor.execute( f'''
            #         UPDATE pertandingan SET id_stadium = \'{stadium}\'
            #         WHERE id_panitia = \'{panitia}\'
            #         and start_datetime = \'{tanggal_waktu_mulai}\'
            #         and end_datetime =  \'{tanggal_waktu_akhir}\';
            #         ''')
            #         connection.commit()
            #         return HttpResponseRedirect(reverse('pertandingan:pertandingan'))
            #     except Exception as e:
            #         connection.rollback()
            #         query1 = f'''
            #         select nama, id_stadium from stadium;
            #         '''
            #         cursor.execute(query1)
            #         stadium = cursor.fetchall()
            #         context = {
            #             'stadium': stadium,
            #             'role':'panitia',
            #             'message':'ERROR, stadium pada tanggal tersebut tidak tersedia'
            #         }
            #         return render(request, 'pilih_peristiwa.html', context)

            query1 = f'''
            select nama, id_stadium from stadium;
            '''
            cursor.execute(query1)
            stadium = cursor.fetchall()

            context = {
                'stadium': stadium,
                'role': 'panitia',
            }

            return render(request, 'pilih_peristiwa.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
