from django.shortcuts import render, redirect
from .forms import CadastroUsuarioForm, PerfilUsuarioForm
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import login
from .models import *
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

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

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CadastroUsuarioForm()
    return render(request, 'registration/cadastro_cliente.html')

def contato_view(request):
    return render(request, 'contato.html') 

def login_view(request):
  
    if request.user.is_authenticated:
        return redirect('home')
        
   
    if request.method == 'POST':

        email_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        

        user = authenticate(request, email=email_digitado, password=senha_digitada)
        
        if user is not None:
            
            login(request, user)
            return redirect('home')
        else:
            
            messages.error(request, 'E-mail ou senha inválidos.')
            
    
    return render(request, 'registration/login_cliente.html')

def logout_view(request):
    logout(request)
    return redirect('home')
#POR ENQUANTO DASHBOARD É PUBLICO PARA TODOS
def dashboard_view(request):
    usuarios = Usuario.objects.all()
    planos = Plano.objects.all()
    
    context = {
        'usuarios': usuarios,
        'planos': planos
    }
    return render(request, 'dashboard.html', context)

@login_required 
def perfil_view(request):
    
    if request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
       
        form = PerfilUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seus dados foram atualizados com sucesso!')
            return redirect('perfil')
    else:
        
        form = PerfilUsuarioForm(instance=request.user)

    return render(request, 'perfil.html', {'form': form})