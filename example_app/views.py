from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def index(request):
    return render(request, 'login_atau_register.html')

def showDashboard(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':
            uuid = request.COOKIES.get('uuid')

            cursor.execute(f'select jabatan from panitia where id_panitia = \'{uuid}\'')

            panitia = cursor.fetchmany()
            jabatan = panitia[0][0]

            query = f"""
                select nama_depan, nama_belakang, nomor_hp, email, alamat
                from non_pemain 
                where id = \'{uuid}\';
            """

            cursor.execute(query)
            non_pemain = cursor.fetchmany()
            nama_depan = non_pemain[0][0]
            nama_belakang = non_pemain[0][1]
            nomor_hp = non_pemain[0][2]
            email = non_pemain[0][3]
            alamat = non_pemain[0][4]


            cursor.execute(
            f'select status from status_non_pemain where id_non_pemain = \'{uuid}\'')
            status_non_pemain = cursor.fetchmany()
            status = status_non_pemain[0][0]

            context = {
                'status': 'success',
                'role': request.COOKIES.get('role'),
                'nama_depan': nama_depan,
                'nama_belakang': nama_belakang,
                'nomor_hp': nomor_hp,
                'email': email,
                'alamat': alamat,
                'status_non_pemain': status,
                'jabatan' : jabatan,
            }

            response = render(request, 'dashboard.html', context)
            return response
        else :
            uuid = request.COOKIES.get('uuid')

            query = f"""
                select nama_depan, nama_belakang, nomor_hp, email, alamat
                from non_pemain 
                where id = \'{uuid}\';
            """

            cursor.execute(query)
            non_pemain = cursor.fetchmany()
            nama_depan = non_pemain[0][0]
            nama_belakang = non_pemain[0][1]
            nomor_hp = non_pemain[0][2]
            email = non_pemain[0][3]
            alamat = non_pemain[0][4]


            cursor.execute(
            f'select status from status_non_pemain where id_non_pemain = \'{uuid}\'')
            status_non_pemain = cursor.fetchmany()
            status = status_non_pemain[0][0]

            context = {
                'status': 'success',
                'role': request.COOKIES.get('role'),
                'nama_depan': nama_depan,
                'nama_belakang': nama_belakang,
                'nomor_hp': nomor_hp,
                'email': email,
                'alamat': alamat,
                'status_non_pemain': status,
            }

            response = render(request, 'dashboard.html', context)
            return response
        
    else:
        return HttpResponseRedirect(reverse('example_app:index'))

def login(request):
    if request.COOKIES.get('role'):
        return HttpResponseRedirect(reverse('example_app:dashboard'))
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        cursor.execute(
            f'select username, password from user_system where username = \'{username}\'')
        user = cursor.fetchmany()

        if(len(user) == 0):
            context = {
                'message': 'Username tidak ditemukan!',
                'status': 'error',
            }
            return render(request, 'login.html', context)
                

        username_database=user[0][0]
        password_database=user[0][1]


        if(username != username_database or password != password_database):
            context = {
                'message': 'Cek kembali username dan password anda!',
                'status': 'error',
            }
            return render(request, 'login.html', context)
        
        else:
            cursor.execute(
            f'select id_manajer from manajer where username = \'{username}\'')
            manajer = cursor.fetchmany()


            if len(manajer) != 0:
                role = 'manajer'
                uuid = manajer[0][0]

                response = HttpResponseRedirect(reverse('example_app:dashboard'))
                response.set_cookie('role', role)
                response.set_cookie('uuid', uuid)
                response.set_cookie('username', username)
                return response
            
            cursor.execute(
            f'select id_penonton from penonton where username = \'{username}\'')
            penonton = cursor.fetchmany()
            
            if len(penonton) != 0:
                role = 'penonton'
                uuid = penonton[0][0]

                response = HttpResponseRedirect(reverse('example_app:dashboard'))
                response.set_cookie('role', role)
                response.set_cookie('uuid', uuid)
                response.set_cookie('username', username)
                return response
            
            cursor.execute(
            f'select id_panitia from panitia where username = \'{username}\'')
            panitia = cursor.fetchmany()
            role = 'panitia'
            uuid = panitia[0][0]

            response = HttpResponseRedirect(reverse('example_app:dashboard'))
            response.set_cookie('role', role)
            response.set_cookie('uuid', uuid)
            response.set_cookie('username', username)
            return response


    return render(request, 'login.html')

def logout_user(request):
    response = HttpResponseRedirect(reverse('example_app:index'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

def register_select(request):
    return render(request, 'register.html')


def register_manajer(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        nomor_hp = request.POST.get('nomor_hp')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        status = request.POST.get('radio_status')

        try:
            # Execute insertion test on username
            cursor.execute(
                f'INSERT INTO user_system (username, password) VALUES (\'{username}\', \'{password}\');'
            )
            connection.commit()
    
        except Exception as e:
            connection.rollback()
            context = {
                'message': 'Username telah digunakan, silahkan gunakan username lain!',
                'status': 'error',
            }
            return render(request, 'register_manajer.html', context)
        
        # Generate UUID
        cursor.execute(
            f'SELECT uuid_generate_v1();'
        )
        uuid = cursor.fetchone()[0]

        # Insert table non pemain
        cursor.execute(
            f'''INSERT INTO Non_Pemain (ID, Nama_Depan, Nama_Belakang, Nomor_HP, Email, Alamat) 
            VALUES (\'{uuid}\', \'{nama_depan}\', \'{nama_belakang}\', \'{nomor_hp}\', \'{email}\', \'{alamat}\');'''
        )
        connection.commit()

        # Insert table manajer
        cursor.execute(
            f'''INSERT INTO Manajer (ID_Manajer, Username) 
            VALUES (\'{uuid}\', \'{username}\');'''
        )
        connection.commit()

        # Insert table status_non_pemain
        cursor.execute(
            f'''INSERT INTO Status_Non_Pemain (ID_Non_Pemain, Status) 
            VALUES (\'{uuid}\', \'{status}\');'''
        )
        connection.commit()

        context = {
            'message': 'Registrasi berhasil, silahkan login kedalam sistem',
            'status': 'registersuccess',
        }
        return render(request, 'login.html', context)
    return render(request, 'register_manajer.html')

def register_penonton(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        nomor_hp = request.POST.get('nomor_hp')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        status = request.POST.get('radio_status')

        try:
            # Execute insertion test on username
            cursor.execute(
                f'INSERT INTO user_system (username, password) VALUES (\'{username}\', \'{password}\');'
            )
            connection.commit()

        except Exception as e:
            connection.rollback()
            context = {
                'message': 'Username telah digunakan, silahkan gunakan username lain!',
                'status': 'error',
            }
            return render(request, 'register_penonton.html', context)
        
        # Generate UUID
        cursor.execute(
            f'SELECT uuid_generate_v1();'
        )
        uuid = cursor.fetchone()[0]

        # Insert table non pemain
        cursor.execute(
            f'''INSERT INTO Non_Pemain (ID, Nama_Depan, Nama_Belakang, Nomor_HP, Email, Alamat) 
            VALUES (\'{uuid}\', \'{nama_depan}\', \'{nama_belakang}\', \'{nomor_hp}\', \'{email}\', \'{alamat}\');'''
        )
        connection.commit()

        # Insert table penonton
        cursor.execute(
            f'''INSERT INTO Penonton (ID_penonton, Username) 
            VALUES (\'{uuid}\', \'{username}\');'''
        )
        connection.commit()

        # Insert table status_non_pemain
        cursor.execute(
            f'''INSERT INTO Status_Non_Pemain (ID_Non_Pemain, Status) 
            VALUES (\'{uuid}\', \'{status}\');'''
        )
        connection.commit()

        context = {
            'message': 'Registrasi berhasil, silahkan login kedalam sistem',
            'status': 'registersuccess',
        }
        return render(request, 'login.html', context)
    return render(request, 'register_penonton.html')

def register_panitia(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        nomor_hp = request.POST.get('nomor_hp')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        status = request.POST.get('radio_status')
        jabatan = request.POST.get('jabatan')

        try:
            # Execute insertion test on username
            cursor.execute(
                f'INSERT INTO user_system (username, password) VALUES (\'{username}\', \'{password}\');'
            )
            connection.commit()

        except Exception as e:
            connection.rollback()
            context = {
                'message': 'Username telah digunakan, silahkan gunakan username lain!',
                'status': 'error',
            }
            return render(request, 'register_panitia.html', context)
        
        # Generate UUID
        cursor.execute(
            f'SELECT uuid_generate_v1();'
        )
        uuid = cursor.fetchone()[0]

        # Insert table non pemain
        cursor.execute(
            f'''INSERT INTO Non_Pemain (ID, Nama_Depan, Nama_Belakang, Nomor_HP, Email, Alamat) 
            VALUES (\'{uuid}\', \'{nama_depan}\', \'{nama_belakang}\', \'{nomor_hp}\', \'{email}\', \'{alamat}\');'''
        )
        connection.commit()

        # Insert table panitia
        cursor.execute(
            f'''INSERT INTO Panitia (ID_panitia, jabatan, Username) 
            VALUES (\'{uuid}\', \'{jabatan}\', \'{username}\');'''
        )
        connection.commit()

        # Insert table status_non_pemain
        cursor.execute(
            f'''INSERT INTO Status_Non_Pemain (ID_Non_Pemain, Status) 
            VALUES (\'{uuid}\', \'{status}\');'''
        )
        connection.commit()

        context = {
            'message': 'Registrasi berhasil, silahkan login kedalam sistem',
            'status': 'registersuccess',
        }
        return render(request, 'login.html', context)
    return render(request, 'register_panitia.html')
        
        
