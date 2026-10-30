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
from .forms import (CadastroUsuarioForm, FotoPerfilForm, EnderecoForm, ServicoForm, PlanoForm, UsuarioAdminForm, ComprovanteForm)
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
        # ... seu código de POST existente ...
        pass # (Mantenha o código original aqui)
    else:
        form_dados = CadastroUsuarioForm(instance=user)
        form_dados.fields['senha'].required = False
        form_foto = FotoPerfilForm(instance=user)
        form_endereco = EnderecoForm(instance=user)

    # --- NOVO: Buscar compras do usuário ---
    # Trazendo em ordem decrescente (mais recentes primeiro) por padrão, 
    # pois o model Compra já tem ordering=['-data_compra']
    compras = user.compras.all()

    context = {
        'form_dados': form_dados,
        'form_foto': form_foto,
        'form_endereco': form_endereco,
        'foto': user.foto,
        'user': user,
        'compras': compras, # <--- Adicione isso
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

# ==========================================
# CARRINHO
# ==========================================

def _get_or_create_carrinho(user):
    """Garante que o usuário tenha um carrinho. Retorna (carrinho, criado)."""
    carrinho, _ = Carrinho.objects.get_or_create(usuario=user)
    return carrinho

@login_required
def carrinho_view(request):
    """
    Página do carrinho com itens, resumo E envio de comprovante na
    mesma tela. O POST do comprovante é tratado aqui, então não é
    mais necessário o usuário ir pra outra URL.
    """
    carrinho = _get_or_create_carrinho(request.user)
    itens = carrinho.itens.select_related('servico', 'plano').all()

    # POST do comprovante vem do form da própria página
    if request.method == 'POST':
        # Se o carrinho está vazio, nem tenta — avisa e volta
        if carrinho.vazio:
            messages.error(request, 'Seu carrinho está vazio.')
            return redirect('carrinho')

        form_comprovante = ComprovanteForm(request.POST, request.FILES)
        if form_comprovante.is_valid():
            comprovante = form_comprovante.save(commit=False)
            comprovante.usuario = request.user
            comprovante.carrinho = carrinho
            comprovante.status = 'pendente'
            comprovante.save()
            messages.success(
                request,
                'Comprovante enviado! Aguarde a análise do nosso time.'
            )
            return redirect('carrinho')
        # se o form tem erros, cai no render lá embaixo com o form inválido
    else:
        form_comprovante = ComprovanteForm(initial={'valor': carrinho.total})

    return render(request, 'carrinho.html', {
        'carrinho': carrinho,
        'itens': itens,
        'form_comprovante': form_comprovante,
    })


@login_required
@require_POST
def carrinho_adicionar_servico(request, servico_id):
    """
    Adiciona 1 serviço ao carrinho.
    - Se o mesmo serviço já estiver no carrinho, não duplica.
    - Faz snapshot de nome/preço/capa no momento da adição.
    """
    servico = get_object_or_404(Servico, pk=servico_id)
    carrinho = _get_or_create_carrinho(request.user)

    ja_existe = carrinho.itens.filter(tipo='servico', servico=servico).exists()

    if ja_existe:
        messages.info(request, 'Este serviço já está no seu carrinho.')
    else:
        ItemCarrinho.objects.create(
            carrinho=carrinho,
            tipo='servico',
            servico=servico,
        )
        messages.success(request, f'"{servico.nome}" adicionado ao carrinho.')

    # Resposta AJAX (se o botão usar fetch) ou redirect normal
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'ok': True,
            'quantidade': carrinho.quantidade_itens,
        })
    return redirect(request.META.get('HTTP_REFERER') or 'services')


@login_required
@require_POST
def carrinho_adicionar_plano(request, plano_id):
    """
    Adiciona 1 plano ao carrinho.
    Regras:
    - Não duplica o mesmo plano.
    - Se o serviço principal do plano já está no carrinho como 'servico',
      bloqueia (evita comprar serviço avulso + plano dele).
    """
    plano = get_object_or_404(Plano.objects.select_related('servico'), pk=plano_id)
    carrinho = _get_or_create_carrinho(request.user)

    ja_existe_plano = carrinho.itens.filter(tipo='plano', plano=plano).exists()
    servico_no_carrinho = carrinho.itens.filter(
        tipo='servico', servico=plano.servico
    ).exists()

    if ja_existe_plano:
        messages.info(request, 'Este plano já está no seu carrinho.')
    elif servico_no_carrinho:
        messages.warning(
            request,
            'Você já adicionou o serviço principal deste plano. '
            'Remova-o antes de escolher um plano específico.'
        )
    else:
        ItemCarrinho.objects.create(
            carrinho=carrinho,
            tipo='plano',
            plano=plano,
        )
        messages.success(request, f'"{plano.nome}" adicionado ao carrinho.')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'ok': True,
            'quantidade': carrinho.quantidade_itens,
        })
    return redirect(request.META.get('HTTP_REFERER') or 'services')


@login_required
@require_POST
def carrinho_remover(request, item_id):
    """Remove um item específico do carrinho do usuário logado."""
    carrinho = _get_or_create_carrinho(request.user)
    item = get_object_or_404(ItemCarrinho, pk=item_id, carrinho=carrinho)

    nome = str(item)
    item.delete()
    messages.success(request, f'"{nome}" removido do carrinho.')
    return redirect('carrinho')

# ---------- CARRINHOS ----------
@superuser_required
def dash_carrinhos(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    # Anota contagens para ordenar/priorizar na tela
    carrinhos = (
        Carrinho.objects
        .select_related('usuario')
        .annotate(
            qtd_itens=Count('itens', distinct=True),
            qtd_pendentes=Count(
                'comprovantes',
                filter=Q(comprovantes__status='pendente'),
                distinct=True,
            ),
            qtd_aprovados=Count(
                'comprovantes',
                filter=Q(comprovantes__status='aprovado'),
                distinct=True,
            ),
        )
        .filter(qtd_itens__gt=0)  # ignora carrinhos vazios
    )

    if q:
        carrinhos = carrinhos.filter(
            Q(usuario__email__icontains=q) |
            Q(usuario__first_name__icontains=q) |
            Q(usuario__last_name__icontains=q)
        )

    # Filtro rápido por status do comprovante
    if status == 'pendente':
        carrinhos = carrinhos.filter(qtd_pendentes__gt=0)
    elif status == 'aprovado':
        carrinhos = carrinhos.filter(qtd_aprovados__gt=0)
    elif status == 'sem_comprovante':
        carrinhos = carrinhos.filter(qtd_pendentes=0, qtd_aprovados=0)

    # PRIORIZAÇÃO:
    # 1) carrinhos com comprovante aprovado (prontos para promover)
    # 2) carrinhos com comprovante pendente (aguardando análise)
    # 3) demais, mais recentes primeiro
    carrinhos = carrinhos.annotate(
        prioridade=(
            models.Case(
                models.When(qtd_aprovados__gt=0, then=models.Value(0)),
                models.When(qtd_pendentes__gt=0, then=models.Value(1)),
                default=models.Value(2),
                output_field=models.IntegerField(),
            )
        )
    ).order_by('prioridade', '-atualizado_em')

    # Totais pra cabeçalho
    total_pendentes = Comprovante.objects.filter(status='pendente').count()
    total_aprovados = Comprovante.objects.filter(status='aprovado').count()

    return render(request, 'dash_carrinhos.html', {
        'carrinhos': carrinhos,
        'q': q,
        'status': status,
        'ativo': 'carrinhos',
        'total_pendentes': total_pendentes,
        'total_aprovados': total_aprovados,
    })

# ---------- DETALHE E AÇÕES DO CARRINHO (ADMIN) ----------
@superuser_required
def dash_carrinho_detalhe(request, pk):
    carrinho = get_object_or_404(Carrinho.objects.select_related('usuario'), pk=pk)
    itens = carrinho.itens.select_related('servico', 'plano').all()
    comprovantes = carrinho.comprovantes.all().order_by('-enviado_em')

    # Verifica se há algum comprovante aprovado pronto para promoção
    comprovante_aprovado = comprovantes.filter(status='aprovado').first()

    return render(request, 'dash_carrinho_detalhe.html', {
        'carrinho': carrinho,
        'itens': itens,
        'comprovantes': comprovantes,
        'comprovante_aprovado': comprovante_aprovado,
        'ativo': 'carrinhos',
    })


@superuser_required
@require_POST
def dash_comprovante_acao(request, pk, acao):
    """Aprova ou rejeita um comprovante."""
    comprovante = get_object_or_404(Comprovante, pk=pk)
    carrinho_id = comprovante.carrinho_id

    if not carrinho_id:
        messages.error(request, 'Este comprovante não está vinculado a um carrinho ativo.')
        return redirect('dash_carrinhos')

    if acao == 'aprovar':
        comprovante.marcar_aprovado(request.user)
        messages.success(request, f'Comprovante de R$ {comprovante.valor} aprovado com sucesso.')
    elif acao == 'rejeitar':
        motivo = request.POST.get('motivo', 'Rejeitado via painel.')
        comprovante.marcar_rejeitado(request.user, motivo=motivo)
        messages.warning(request, 'Comprovante rejeitado.')
    else:
        messages.error(request, 'Ação inválida.')
    
    return redirect('dash_carrinho_detalhe', pk=carrinho_id)


@superuser_required
@require_POST
def dash_carrinho_promover(request, pk):
    """Converte o carrinho em Compra(s) e limpa o carrinho."""
    carrinho = get_object_or_404(Carrinho, pk=pk)
    comprovante_id = request.POST.get('comprovante_id')
    
    comprovante = None
    if comprovante_id:
        comprovante = get_object_or_404(Comprovante, pk=comprovante_id, carrinho=carrinho)

    try:
        compras = carrinho.promover_para_compra(request.user, comprovante=comprovante)
        messages.success(
            request, 
            f'Carrinho promovido com sucesso! {len(compras)} compra(s) gerada(s).'
        )
        # Redireciona para a lista de carrinhos (pois este ficará vazio e sumirá da lista)
        return redirect('dash_carrinhos')
    except ValueError as e:
        messages.error(request, f'Erro ao promover: {str(e)}')
        return redirect('dash_carrinho_detalhe', pk=carrinho.pk)


# ---------- ASSINATURAS (PLANOS DOS CLIENTES) ----------
@superuser_required
def dash_assinaturas(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    # Filtra apenas compras do tipo 'plano'
    assinaturas = Compra.objects.select_related('usuario', 'servico', 'plano').filter(tipo='plano')

    if q:
        assinaturas = assinaturas.filter(
            Q(usuario__email__icontains=q) |
            Q(usuario__first_name__icontains=q) |
            Q(usuario__last_name__icontains=q) |
            Q(nome_servico__icontains=q) |
            Q(nome_plano__icontains=q)
        )

    if status == 'ativo':
        assinaturas = assinaturas.filter(ativo=True)
    elif status == 'inativo':
        assinaturas = assinaturas.filter(ativo=False)

    # Ordena pelos mais recentes
    assinaturas = assinaturas.order_by('-data_compra')

    return render(request, 'dash_assinaturas.html', {
        'assinaturas': assinaturas,
        'q': q,
        'status': status,
        'ativo': 'assinaturas',
    })

@superuser_required
@require_POST
def dash_assinatura_toggle(request, pk):
    """Alterna o status (Ativo/Inativo) de uma assinatura (Compra de plano)."""
    compra = get_object_or_404(Compra, pk=pk, tipo='plano')
    
    compra.ativo = not compra.ativo
    compra.save()
    
    status_msg = "ativada" if compra.ativo else "desativada"
    messages.success(request, f'A assinatura do plano "{compra.nome_plano}" foi {status_msg} com sucesso.')
    
    return redirect(request.META.get('HTTP_REFERER') or 'dash_assinaturas')