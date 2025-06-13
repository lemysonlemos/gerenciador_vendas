from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import LoginForm


def inicio(request):
    return render(request, 'autenticacao/inicio.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=f"{cpf}_cliente", password=senha)
            if user is not None and user.is_active:
                auth_login(request, user)
                return redirect('cliente:painel')
            else:
                messages.error(request, 'CPF ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'autenticacao/login.html', {'form': form})




