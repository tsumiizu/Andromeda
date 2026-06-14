from django.urls import path
from . import views
urlpatterns = [
    # Views publicas 
    path('', views.homeview, name='home'),
    path('services/', views.servicesview, name='services'),
    path('contato/', views.contato_view, name='contato'),
    path('equipe/', views.equipeview, name='equipe'),
]