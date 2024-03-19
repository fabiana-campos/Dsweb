from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('DSWEB 2024.1 <br> Matricula: 20231014040033 <br> Fabiana Campos')