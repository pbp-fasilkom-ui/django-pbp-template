from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def index(request):
    return render(request, 'login_atau_register.html')

def showDashboard(request):
    return render(request, 'dashboard.html')

def login(request):
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
                    'role': role,
                    'nama_depan': nama_depan,
                    'nama_belakang': nama_belakang,
                    'nomor_hp': nomor_hp,
                    'email': email,
                    'alamat': alamat,
                    'status_non_pemain': status,
                }

                response = render(request, 'dashboard.html', context)
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

                context = {
                    'status': 'success',
                    'username': user[0][0],
                    'password': user[0][1],
                    'role': role
                }

                response = render(request, 'dashboard.html', context)
                response.set_cookie('role', role)
                response.set_cookie('uuid', uuid)
                response.set_cookie('username', username)
                return response
            
            cursor.execute(
            f'select id_panitia from panitia where username = \'{username}\'')
            panitia = cursor.fetchmany()
            role = 'panitia'
            uuid = penonton[0][0]

            context = {
                'status': 'success',
                'username': user[0][0],
                'password': user[0][1],
                'role': role
            }

            response = render(request, 'dashboard.html', context)
            response.set_cookie('role', role)
            response.set_cookie('uuid', uuid)
            response.set_cookie('username', username)
            return response


    return render(request, 'login.html')

    

