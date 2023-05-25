from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt 
def show_page(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':
            if request.method == 'POST':
                id_stadium = request.POST.get('stadium-select', False)
                date = request.POST.get('date-picker') 
                wasit_utama = request.POST.get('wasit-utama', False)
                wasit_pembantu1 = request.POST.get('wasit-pembantu1', False)
                wasit_pembantu2 = request.POST.get('wasit-pembantu2', False)
                wasit_cadangan = request.POST.get('wasit-cadangan', False)
                tim1 = request.POST.get('tim1', False)
                tim2 = request.POST.get('tim2', False)
                
                cursor.execute(
                    f'SELECT uuid_generate_v1();'
                )
                uuid = cursor.fetchone()[0]

                try:
                    cursor.execute(
                        f"""
                        INSERT INTO PERTANDINGAN (ID_Pertandingan, Start_Datetime, End_Datetime, Stadium) VALUES
                        (\'{uuid}\', '{date} 13:00:00', '{date} 16:00:00', \'{id_stadium}\');
                        """
                    )
                    connection.commit()
                    
                except Exception as e:
                    connection.rollback()
                    print(str(e))
                    return HttpResponseRedirect(reverse('pembuatan_pertandingan:show_page'))
            
                try:
                    cursor.execute(
                        f"""
                        INSERT INTO TIM_PERTANDINGAN (Nama_Tim, ID_Pertandingan, Skor) VALUES
                        (\'{tim1}\', \'{uuid}\', '0'),
                        (\'{tim2}\', \'{uuid}\', '0');
                        """
                    )
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    print('INSERT INTO TIM_PERTANDINGAN EXCEPTION')
                    return HttpResponseRedirect(reverse('pembuatan_pertandingan:show_page'))
                
                try:
                    cursor.execute(
                        f"""
                        INSERT INTO WASIT_BERTUGAS (ID_Wasit, ID_Pertandingan, Posisi_Wasit) VALUES
                        (\'{wasit_utama}\', \'{uuid}\', 'utama'),
                        (\'{wasit_cadangan}\', \'{uuid}\', 'cadangan'),
                        (\'{wasit_pembantu1}\', \'{uuid}\', 'hakim garis'),
                        (\'{wasit_pembantu2}\', \'{uuid}\', 'hakim garis');
                        """
                    )
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    print('INSERT INTO TIM_PERTANDINGAN EXCEPTION')
                    return HttpResponseRedirect(reverse('pembuatan_pertandingan:show_page'))
                
                return HttpResponseRedirect(reverse('pembuatan_pertandingan:show_page'))
            
            cursor.execute(f"""
            select array_to_string(array_agg("nama_tim"),' VS ') as tim_bertanding, pertandingan.id_pertandingan
            from pertandingan, tim_pertandingan, stadium
            where tim_pertandingan.id_pertandingan = pertandingan.id_pertandingan and pertandingan.stadium = stadium.id_stadium
            group by pertandingan.start_datetime, stadium.nama, pertandingan.id_pertandingan
            order by pertandingan.start_datetime;
            """)
            tim_bertanding = cursor.fetchall()
            grup_a = tim_bertanding[0:4]
            grup_b = tim_bertanding[4:8]
            grup_c = tim_bertanding[8:12]
            grup_d = tim_bertanding[12:16]
            add_pointer = ''
            if len(grup_d) < 4:
                add_pointer = 'd'
            if len(grup_c) < 4:
                add_pointer = 'c'
            if len(grup_b) < 4:
                add_pointer = 'b'
            if len(grup_a) < 4:
                add_pointer = 'a'

            cursor.execute(f"""
            select nama, id_stadium from stadium;
            """)
            
            list_stadium = cursor.fetchall()

            cursor.execute(f"""
            select w.id_wasit, concat(np.nama_depan, ' ' , np.nama_belakang)
            from wasit w, non_pemain np
            where w.id_wasit = np.id; 
            """)
            
            list_wasit = cursor.fetchall()

            cursor.execute(f"""
            select nama_tim
            from tim;
            """)
            
            list_tim = cursor.fetchall()


            context = {
                'grup_a': grup_a,
                'grup_b': grup_b,
                'grup_c': grup_c,
                'grup_d': grup_d,
                'add_pointer': add_pointer,
                'list_stadium': list_stadium,
                'list_wasit': list_wasit,
                'list_tim': list_tim,
                'role':'panitia',
            }
            return render(request, 'pembuatanpertandingan.html', context)
        return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))

def delete_pertandingan(request, id_pertandingan):
    try:
        cursor.execute(f"Delete From wasit_bertugas where id_pertandingan = \'{id_pertandingan}\'")
        connection.commit()
        cursor.execute(f"Delete From tim_pertandingan where id_pertandingan = \'{id_pertandingan}\'")
        connection.commit()
        cursor.execute(f"Delete From Pertandingan where id_pertandingan = \'{id_pertandingan}\'")
        connection.commit()

    except Exception as e:
        print(str(e))
        connection.rollback()
        return HttpResponseRedirect(reverse('pembuatan_pertandingan:show_page'))

    return HttpResponseRedirect(reverse('pembuatan_pertandingan:show_page'))
