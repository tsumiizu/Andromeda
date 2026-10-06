from django.shortcuts import render, redirect
from .forms import CadastroUsuarioForm, FotoPerfilForm, EnderecoForm
from django_ratelimit.decorators import ratelimit
from .models import *
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

def homeview(request):
    return render(request, 'home.html')

def servicesview(request):
   
    servicos = Servico.objects.prefetch_related('planos').order_by('ordem', 'id')
    
    planos = Plano.objects.all().order_by('preco')
    
    return render(request, 'services.html', {
        'servicos': servicos, 
        'planos': planos
    })

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

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
@staff_member_required
def dashboard_view(request):
    usuarios = Usuario.objects.all()
    planos = Plano.objects.all()
    servicos = Servico.objects.all()  # <--- Garanta que esta busca existe

    context = {
        'usuarios': usuarios,
        'planos': planos,
        'servicos': servicos,  # <--- Garanta que a chave 'servicos' está no contexto
    }
    
    return render(request, 'dashboard.html', context)

def p404_customizada(request, exception):
    return render(request, '404.html', status=404)
# Pagina 403
def p505_customizada(request, exception=None):
    return render(request, '505.html', status=505)

@login_required 
def perfil_view(request):
    user = request.user

    if request.method == 'POST':
        form_dados = CadastroUsuarioForm(request.POST, instance=user)
        form_foto = FotoPerfilForm(request.POST, request.FILES, instance=user)
        form_endereco = EnderecoForm(request.POST, instance=user)
        form_dados.fields['senha'].required = False
        if form_dados.is_valid() and form_foto.is_valid() and form_endereco.is_valid():
            form_dados.save()
            form_foto.save()
            form_endereco.save()
            if form_dados.cleaned_data.get('senha'):
                update_session_auth_hash(request, user)

            messages.success(request, 'Seus dados foram atualizados com sucesso!')
            return redirect('perfil')
    else:
        form_dados = CadastroUsuarioForm(instance=user)
        form_dados.fields['senha'].required = False
        form_foto = FotoPerfilForm(instance=user)
        form_endereco = EnderecoForm(instance=user)

    context = {
        'form_dados': form_dados,
        'form_foto': form_foto,
        'form_endereco': form_endereco,
        'foto': user.foto,
        'user': user,
    }
    return render(request, 'perfil.html', context)