from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *

def homeview(request):
    return render(request, 'home.html')
def servicesview(request):
    planos = Plano.objects.all()
    context = {
        'planos': planos
    }
    return render(request, 'services.html', context)
def equipeview(request):
    return render(request, 'equipe.html')
def cadastroview(request):
    return render(request, 'cadastro_cliente.html')
def contato_view(request):
    return render(request, 'contato.html') 