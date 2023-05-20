from django.urls import path
from example_app.views import *

app_name = 'example_app'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('dashboard/', showDashboard, name='dashboard'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_select, name='register'),
    path('register/manajer/', register_manajer, name='register_manajer'),
    path('register/penonton/', register_penonton, name='register_penonton'),
    path('register/panitia/', register_panitia, name='register_panitia'),

]