from django.shortcuts import render
from utils.query import *

def index(request):
    cursor.execute(
        f"SELECT * FROM STADIUM;"
    )
    record = cursor.fetchall()
    
    context = {
        'record' : record
    }
    return render(request, 'index.html', context)
