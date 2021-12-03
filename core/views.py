from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

# Create your views here.
from django.urls import reverse


def index(request):
    return render(request, 'core/index.html')


def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))
