
from django.shortcuts import render

def homeview(request):
    return render(request, 'home.html')
def servicesview(request):
    return render(request, 'services.html')
def equipeview(request):
    return render(request, 'equipe.html')

import requests
from django.shortcuts import render, redirect
from django.contrib import messages

def contato_view(request):
    return render(request, 'contato.html') 