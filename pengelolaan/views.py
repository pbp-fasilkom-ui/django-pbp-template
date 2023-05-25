from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def registrasi_tim(request): 
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':
            
            if request.method == "POST":
                nama_tim = request.POST.get('nama_tim')
                nama_univ = request.POST.get('nama_univ')
                id_manajer = request.COOKIES.get('uuid')
                
                try:
                    cursor.execute(f'''
                    INSERT INTO TIM (Nama_Tim, Universitas) VALUES
                        (\'{nama_tim}\', \'{nama_univ}\');
                    ''')
                    
                    cursor.execute(f'''
                    INSERT INTO TIM_MANAJER (ID_Manajer, Nama_Tim) VALUES
	                    (\'{id_manajer}\', \'{nama_tim}\');
                    ''')
                    
                    connection.commit()
                    return redirect(reverse('pengelolaan:tim'))
                    
                except Exception as e:
                    connection.rollback()
                    context = {
                        'message' : 'Tim sudah terdaftar',
                        'role' : 'manajer'
                    }
                    
                    return render(request, 'registrasi-tim.html', context)
            
            message = request.GET.get('message')
            
            context = {
                'role': 'manajer',
                'message' : message
            }
            
            return render(request, 'registrasi-tim.html', context)
        
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))       

@csrf_exempt
def tim(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':
            
            manajer = request.COOKIES.get('uuid')
            
            query1 = f'''
            SELECT nama_tim FROM tim_manajer WHERE id_manajer = \'{manajer}\';
            '''
            cursor.execute(query1)
            nama_tim = cursor.fetchone()
            
            if nama_tim is None:
                return redirect('pengelolaan:registrasi_tim')
            
            else:
                nama_tim = nama_tim[0]
                cursor.execute(f'''
                SELECT id_pemain, nama_depan || ' ' || nama_belakang AS nama_pemain, nomor_hp, tgl_lahir, is_captain, posisi, npm, jenjang
                FROM pemain
                WHERE nama_tim = \'{nama_tim}\'
                ORDER BY npm ASC;
                ''')
                
                daftar_pemain = cursor.fetchall()
                
                cursor.execute(f'''
                SELECT P.id_pelatih, NP.nama_depan || ' ' || NP.nama_belakang AS nama_pelatih, NP.nomor_hp, NP.email, NP.alamat, SP.spesialisasi
                FROM pelatih P
                JOIN non_pemain NP ON P.id_pelatih = NP.id
                JOIN spesialisasi_pelatih SP ON P.id_pelatih = SP.id_pelatih
                WHERE P.nama_tim = \'{nama_tim}\';
                ''')
                
                daftar_pelatih = cursor.fetchall()
                message = request.COOKIES.get('message')
                
                context = {
                    'nama_tim' : nama_tim,
                    'daftar_pemain': daftar_pemain,
                    'daftar_pelatih': daftar_pelatih,
                    'role':'manajer',
                    'message' : message
                }
                
                response = render(request, 'tim.html', context)
                response.delete_cookie('message')
                
                return response
            
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))   
           

@csrf_exempt
def tambah_pelatih(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':

            if request.method == "POST":
                pelatih = request.POST.get('pelatih')
                manajer = request.COOKIES.get('uuid')
                
                query1 = f'''
                SELECT nama_tim FROM tim_manajer WHERE id_manajer = \'{manajer}\';
                '''
                cursor.execute(query1)
                nama_tim_manajer = cursor.fetchone()[0]
                
                try:
                    cursor.execute( f'''
                    UPDATE pelatih 
                    SET nama_tim = \'{nama_tim_manajer}\'
                    WHERE id_pelatih = \'{pelatih}\';
                    ''')
                    connection.commit()
                    
                    response = redirect(reverse('pengelolaan:tim'))
                    response.set_cookie('message', 'Berhasil Menambahkan Pelatih Baru')
            
                    return response
                
                except Exception as e:
                    connection.rollback()
                    
                    cursor.execute(f'''
                    SELECT P.id_pelatih, NP.nama_depan || ' ' || NP.nama_belakang AS nama_pelatih, SP.spesialisasi
                    FROM pelatih P
                    JOIN non_pemain NP ON P.id_pelatih = NP.id
                    JOIN spesialisasi_pelatih SP ON P.id_pelatih = SP.id_pelatih
                    WHERE P.nama_tim = 'tim_ghaib';
                    ''')
                    
                    pelatih_available = cursor.fetchall()
                    
                    context = {
                        'message' : str(e).split(".")[0],
                        'role' : 'manajer',
                        'pelatih': pelatih_available
                    }
                    
                    return render(request, 'tambah-pelatih.html', context)
                
    cursor.execute(f'''
    SELECT P.id_pelatih, NP.nama_depan || ' ' || NP.nama_belakang AS nama_pelatih, SP.spesialisasi
    FROM pelatih P
    JOIN non_pemain NP ON P.id_pelatih = NP.id
    JOIN spesialisasi_pelatih SP ON P.id_pelatih = SP.id_pelatih
    WHERE P.nama_tim = 'tim_ghaib';
    ''')
    
    pelatih_available = cursor.fetchall()
    
    context = {
        'pelatih': pelatih_available,
        'role':'manajer',
    }
    
    return render(request, 'tambah-pelatih.html', context)

@csrf_exempt
def tambah_pemain(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'manajer':

            if request.method == "POST":
                pemain = request.POST.get('pemain')
                manajer = request.COOKIES.get('uuid')
                
                query1 = f'''
                SELECT nama_tim FROM tim_manajer WHERE id_manajer = \'{manajer}\';
                '''
                cursor.execute(query1)
                nama_tim_manajer = cursor.fetchone()[0]
                
                try:
                    cursor.execute(f'''
                    UPDATE pemain 
                    SET nama_tim = \'{nama_tim_manajer}\',
                    is_captain = false
                    WHERE id_pemain = \'{pemain}\';
                    ''')
                    connection.commit()
                    
                    response = redirect(reverse('pengelolaan:tim'))
                    response.set_cookie('message', 'Berhasil Menambahkan Pemain Baru')
            
                    return response
                
                except Exception as e:
                    connection.rollback()
                    context = {
                        'message' : 'ERROR, gagal menambahkan pemain baru',
                        'role' : 'manajer'
                    }
                    return render(request, 'tambah-pemain.html', context)
                                    
    query1 = f'''
    select id_pemain, nama_depan, nama_belakang, posisi 
    from pemain 
    where nama_tim = 'tim_ghaib';
    '''
    cursor.execute(query1)
    pemain_available = cursor.fetchall()
    message = request.GET.get('message')
     
    context = {
        'pemain': pemain_available,
        'role':'manajer',
        'message': message,
    }
    
    return render(request, 'tambah-pemain.html', context)

@csrf_exempt
def make_captain(request):
    if request.method == 'POST':
        id_pemain = request.POST.get('id_pemain')
        
        try:
            cursor.execute(f'''
            UPDATE pemain
            SET is_captain = true
            WHERE id_pemain = \'{id_pemain}\';   
            ''')
            connection.commit()
            
            response = redirect(reverse('pengelolaan:tim'))
            response.set_cookie('message', 'Berhasil Mengubah Kapten')
            
            return response
        
        except Exception as e:
            connection.rollback()
            
            response = redirect(reverse('pengelolaan:tim'))
            response.set_cookie('message', 'ERROR: Kapten tidak berubah')
            
            return response
            
    return HttpResponseRedirect(reverse('pengelolaan:tim'))

@csrf_exempt
def delete_pemain(request):
    if request.method == "POST":
        pemain = request.POST.get('id_pemain')
        
        try:
            cursor.execute(f'''
            UPDATE pemain 
            SET nama_tim = 'tim_ghaib',
            is_captain = false
            WHERE id_pemain = \'{pemain}\';
            ''')
            connection.commit()
            
            response = redirect(reverse('pengelolaan:tim'))
            response.set_cookie('message', 'Berhasil Menghapus Pemain')
    
            return response
        
        except Exception as e:
            connection.rollback()
            
            response = redirect(reverse('pengelolaan:tim'))
            response.set_cookie('message', 'ERROR: Tidak bisa menghapus pemain')
            
            return response
                            
    return HttpResponseRedirect(reverse('pengelolaan:tim'))

@csrf_exempt
def delete_pelatih(request):
    if request.method == "POST":
        pelatih = request.POST.get('id_pelatih')
        
        try:
            cursor.execute(f'''
            UPDATE pelatih 
            SET nama_tim = 'tim_ghaib'
            WHERE id_pelatih = \'{pelatih}\';
            ''')
            
            connection.commit()
            
            response = redirect(reverse('pengelolaan:tim'))
            response.set_cookie('message', 'Berhasil Menghapus Pelatih')
    
            return response
        
        except Exception as e:
            connection.rollback()
            
            response = redirect(reverse('pengelolaan:tim'))
            response.set_cookie('message', 'ERROR: Tidak bisa menghapus pelatih')
            
            return response
                            
    return HttpResponseRedirect(reverse('pengelolaan:tim'))