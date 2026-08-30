from django.shortcuts import render, redirect
from .forms import CadastroUsuarioForm
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import login
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

@ratelimit(key='ip', rate='5/m', block=True)
def cadastroview(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CadastroUsuarioForm()
    return render(request, 'cadastro.html')

def contato_view(request):
    return render(request, 'contato.html') 