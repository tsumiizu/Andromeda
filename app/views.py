from django.shortcuts import render, redirect
from .forms import CadastroUsuarioForm, FotoPerfilForm, EnderecoForm
from django_ratelimit.decorators import ratelimit
from .models import *
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (CadastroUsuarioForm, FotoPerfilForm, EnderecoForm,
                    ServicoForm, PlanoForm, UsuarioAdminForm)

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



from django.shortcuts import render

def portfolio_view(request):
    # Lista contendo os projetos da empresa (atualmente configurado com 1 projeto)
    projects = [
        {
            'title': 'Projeto ManiaGeek',
            'description': 'Plataforma web avançada desenvolvida com foco em alta performance, design responsivo e interface imersiva para e-commerce.',
            'image_url': 'media/maniageek.png',
            'site_url': 'https://maniageek.onrender.com/', # Substitua pelo link real do seu site feito
            'tags': ['Django', 'Python', 'CSS3', 'JavaScript']
        }
    ]
    return render(request, 'portfolio.html', {'projects': projects})


# ==========================================
# DASHBOARD: gerenciamento (somente superuser)
# ==========================================
def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


# ---------- SERVIÇOS ----------
@superuser_required
def dash_servicos(request):
    q = request.GET.get('q', '').strip()
    servicos = Servico.objects.annotate(qtd_planos=Count('planos')).order_by('ordem', 'id')
    if q:
        servicos = servicos.filter(nome__icontains=q)
    return render(request, 'dash_servicos.html', {'servicos': servicos, 'q': q, 'ativo': 'servicos'})


@superuser_required
def dash_servico_form(request, pk=None):
    servico = get_object_or_404(Servico, pk=pk) if pk else None
    form = ServicoForm(request.POST or None, request.FILES or None, instance=servico)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Serviço salvo com sucesso!')
        return redirect('dash_servicos')
    return render(request, 'dash_form.html', {
        'form': form,
        'ativo': 'servicos',
        'titulo': 'Editar serviço' if servico else 'Novo serviço',
        'voltar': 'dash_servicos',
        'preview': servico.capa_url if servico else None,
    })


@superuser_required
def dash_servico_excluir(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        try:
            servico.delete()
            messages.success(request, 'Serviço excluído.')
        except ProtectedError:
            messages.error(request, 'Não é possível excluir: existem compras vinculadas a este serviço ou aos planos dele.')
        return redirect('dash_servicos')
    return render(request, 'dash_excluir.html', {
        'ativo': 'servicos',
        'titulo': 'Excluir serviço',
        'obj_nome': servico.nome,
        'aviso': 'Todos os planos deste serviço também serão excluídos.',
        'voltar': 'dash_servicos',
    })


# ---------- PLANOS ----------
@superuser_required
def dash_planos(request):
    q = request.GET.get('q', '').strip()
    planos = Plano.objects.select_related('servico').order_by('servico__nome', 'preco')
    if q:
        planos = planos.filter(Q(nome__icontains=q) | Q(servico__nome__icontains=q))
    return render(request, 'dash_planos.html', {'planos': planos, 'q': q, 'ativo': 'planos'})


@superuser_required
def dash_plano_form(request, pk=None):
    plano = get_object_or_404(Plano, pk=pk) if pk else None
    form = PlanoForm(request.POST or None, request.FILES or None, instance=plano)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Plano salvo com sucesso!')
        return redirect('dash_planos')
    return render(request, 'dash_form.html', {
        'form': form,
        'ativo': 'planos',
        'titulo': 'Editar plano' if plano else 'Novo plano',
        'voltar': 'dash_planos',
        'preview': plano.capa_url if plano else None,
    })


@superuser_required
def dash_plano_excluir(request, pk):
    plano = get_object_or_404(Plano, pk=pk)
    if request.method == 'POST':
        try:
            plano.delete()
            messages.success(request, 'Plano excluído.')
        except ProtectedError:
            messages.error(request, 'Não é possível excluir: existem compras vinculadas a este plano.')
        return redirect('dash_planos')
    return render(request, 'dash_excluir.html', {
        'ativo': 'planos',
        'titulo': 'Excluir plano',
        'obj_nome': plano.nome,
        'aviso': 'Essa ação não pode ser desfeita.',
        'voltar': 'dash_planos',
    })


# ---------- USUÁRIOS ----------
@superuser_required
def dash_usuarios(request):
    q = request.GET.get('q', '').strip()
    usuarios = Usuario.objects.annotate(qtd_compras=Count('compras')).order_by('-date_joined')
    if q:
        usuarios = usuarios.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
        )
    return render(request, 'dash_usuarios.html', {'usuarios': usuarios, 'q': q, 'ativo': 'usuarios'})


@superuser_required
def dash_usuario_editar(request, pk):
    alvo = get_object_or_404(Usuario, pk=pk)
    form = UsuarioAdminForm(request.POST or None, instance=alvo)
    if alvo == request.user:  # evita se trancar para fora do painel
        form.fields['is_active'].disabled = True
        form.fields['is_staff'].disabled = True
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('dash_usuarios')
    return render(request, 'dash_form.html', {
        'form': form,
        'ativo': 'usuarios',
        'titulo': 'Editar usuário',
        'voltar': 'dash_usuarios',
        'preview': alvo.foto_url,
    })


@superuser_required
def dash_usuario_excluir(request, pk):
    alvo = get_object_or_404(Usuario, pk=pk)
    if alvo == request.user or alvo.is_superuser:
        messages.error(request, 'Você não pode excluir a si mesmo nem outro superusuário.')
        return redirect('dash_usuarios')
    if request.method == 'POST':
        alvo.delete()
        messages.success(request, 'Usuário excluído.')
        return redirect('dash_usuarios')
    return render(request, 'dash_excluir.html', {
        'ativo': 'usuarios',
        'titulo': 'Excluir usuário',
        'obj_nome': alvo.email,
        'aviso': 'Todas as compras deste usuário também serão excluídas. Se só quiser bloquear o acesso, desmarque "Conta ativa" na edição.',
        'voltar': 'dash_usuarios',
    })