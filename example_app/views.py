from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def index(request):
    return render(request, 'login_atau_register.html')
 
def login(request):
    return render(request, 'login.html')

