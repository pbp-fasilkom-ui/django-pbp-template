from django.urls import path
from example_app.views import *

app_name = 'example_app'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('dashboard/', showDashboard, name='dashboard')
]