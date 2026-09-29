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
]