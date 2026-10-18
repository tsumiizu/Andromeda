from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Views publicas 
    path('', views.homeview, name='home'),
    path('services/', views.servicesview, name='services'),
    path('contato/', views.contato_view, name='contato'),
    path('equipe/', views.equipeview, name='equipe'),
    path('cadastro/', views.cadastroview, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    # Dashboard: gerenciamento (superuser)
    path('dashboard/servicos/', views.dash_servicos, name='dash_servicos'),
    path('dashboard/servicos/novo/', views.dash_servico_form, name='dash_servico_novo'),
    path('dashboard/servicos/<int:pk>/editar/', views.dash_servico_form, name='dash_servico_editar'),
    path('dashboard/servicos/<int:pk>/excluir/', views.dash_servico_excluir, name='dash_servico_excluir'),

    path('dashboard/planos/', views.dash_planos, name='dash_planos'),
    path('dashboard/planos/novo/', views.dash_plano_form, name='dash_plano_novo'),
    path('dashboard/planos/<int:pk>/editar/', views.dash_plano_form, name='dash_plano_editar'),
    path('dashboard/planos/<int:pk>/excluir/', views.dash_plano_excluir, name='dash_plano_excluir'),

    path('dashboard/usuarios/', views.dash_usuarios, name='dash_usuarios'),
    path('dashboard/usuarios/<int:pk>/editar/', views.dash_usuario_editar, name='dash_usuario_editar'),
    path('dashboard/usuarios/<int:pk>/excluir/', views.dash_usuario_excluir, name='dash_usuario_excluir'),
]