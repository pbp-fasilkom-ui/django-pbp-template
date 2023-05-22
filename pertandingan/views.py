from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


def get_peristiwa(id_pertandingan, nama_tim):
    get_peristiwa_tim = f'''
                SELECT CONCAT(nama_depan, ' ', nama_belakang), jenis     
                FROM PEMAIN NATURAL JOIN PERISTIWA
                WHERE nama_tim = \'{nama_tim}\' AND
                ID_pertandingan = \'{id_pertandingan}\';
            '''
    cursor.execute(get_peristiwa_tim)
    peristiwa_tim = cursor.fetchall()
    if (len(peristiwa_tim) <= 0):
        peristiwa_tim = [("none", "none")]
    return peristiwa_tim


def get_pemain(nama_tim):
    get_pemain_tim = f'''
        SELECT ID_pemain, CONCAT(nama_depan, ' ', nama_belakang) AS nama     
        FROM PEMAIN
        WHERE nama_tim = \'{nama_tim}\';
    '''
    cursor.execute(get_pemain_tim)
    pemain = cursor.fetchall()
    if (len(pemain) <= 0):
        pemain = [("none", "none")]
    return pemain


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

                datetime_pertandingan = datetime.now() + timedelta(minutes=4)  # for testing
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
                nama_tim1 = tim_pertandingan[0][1] if tim_pertandingan[0][1] else "-"
                nama_tim2 = tim_pertandingan[1][1] if tim_pertandingan[1][1] else "-"
                skor_tim1 = tim_pertandingan[0][0] if tim_pertandingan[0][0] else "-"
                skor_tim2 = tim_pertandingan[1][0] if tim_pertandingan[1][0] else "-"

                peristiwa_tim1 = get_peristiwa(UUID_pertandingan, nama_tim1)
                peristiwa_tim2 = get_peristiwa(UUID_pertandingan, nama_tim2)

                pemenang = nama_tim2 if skor_tim1 > skor_tim2 else nama_tim1

                pertandingan_fix = (
                    datetime_pertandingan, nama_tim1, nama_tim2, status, pemenang, peristiwa_tim1, peristiwa_tim2, UUID_pertandingan)
                daftar_pertandingan_fix.append(pertandingan_fix)

            context = {
                'daftar_pertandingan': daftar_pertandingan_fix,
                'role': 'panitia',
            }

            return render(request, 'mengelola_pertandingan.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))


def mulai_pertandingan(request, id_pertandingan):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':

            get_tim_pertandingan = f'''
                SELECT skor, nama_tim
                FROM TIM_PERTANDINGAN
                WHERE ID_pertandingan =  \'{id_pertandingan}\';
            '''
            cursor.execute(get_tim_pertandingan)
            tim_pertandingan = cursor.fetchmany(2)
            nama_tim1 = tim_pertandingan[0][1]
            nama_tim2 = tim_pertandingan[1][1]

            peristiwa_tim1 = get_peristiwa(id_pertandingan, nama_tim1)
            peristiwa_tim2 = get_peristiwa(id_pertandingan, nama_tim2)

            context = {
                'id_pertandingan': id_pertandingan,
                'tim1': nama_tim1,
                'tim2': nama_tim2,
                'role': 'panitia',
            }

            return render(request, 'mulai_pertandingan.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))


def pilih_peristiwa(request, id_pertandingan, nama_tim):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':

            daftar_pemain = get_pemain(nama_tim)
            peristiwa = get_peristiwa(id_pertandingan, nama_tim)

            if request.method == "POST":
                
                input_id_pemain = request.POST.get('pemain')
                input_jenis_peristiwa = request.POST.get('jenis')

                # tanggal_pinjam = tanggal

                # stadium = request.POST.get('stadium')

                # cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '0 hour' as tanggal;")
                # tanggal_waktu_mulai = cursor.fetchall()[0][0]

                # cursor.execute(f"select TIMESTAMP \'{tanggal_pinjam}\' + interval '3 hour' as tanggal;")
                # tanggal_waktu_akhir = cursor.fetchall()[0][0]

                # panitia = request.COOKIES.get('uuid')

                # try:
                #     cursor.execute( f'''
                #     UPDATE pertandingan SET id_stadium = \'{stadium}\'
                #     WHERE id_panitia = \'{panitia}\'
                #     and start_datetime = \'{tanggal_waktu_mulai}\'
                #     and end_datetime =  \'{tanggal_waktu_akhir}\';
                #     ''')
                #     connection.commit()
                #     return HttpResponseRedirect(reverse('pertandingan:pertandingan'))
                # except Exception as e:
                #     connection.rollback()
                #     query1 = f'''
                #     select nama, id_stadium from stadium;
                #     '''
                #     cursor.execute(query1)
                #     stadium = cursor.fetchall()
                context = {
                    'daftar_peristiwa': peristiwa,
                    'daftar_pemain': daftar_pemain,
                    'nama_tim': nama_tim,
                    'request': request.POST.get('jenis'),
                    'role': 'panitia',
                }
                return render(request, 'pilih_peristiwa.html', context)



            context = {
                'daftar_peristiwa': peristiwa,
                'daftar_pemain': daftar_pemain,
                'nama_tim': nama_tim,
                'role': 'panitia',
            }

            return render(request, 'pilih_peristiwa.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))
