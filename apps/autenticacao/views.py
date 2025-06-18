from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import logout

from .forms import LoginForm
from ..cliente.forms import EsqueceuSenhaForm
from ..cliente.models import Cliente
from ..vinculos.domain import VinculoDomain



def inicio(request):
    logout(request)
    return render(request, 'autenticacao/inicio.html')

def login(request):
    logout(request)
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


def login_funcionario(request):
    logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            if not VinculoDomain.vinculo_ativo(cpf):
                messages.error(request, 'Vinculo inativo')
                return redirect('inicio')
            else:
                senha = form.cleaned_data['senha']
                user = authenticate(request, username=f"{cpf}_cliente", password=senha)
                if user is not None and user.is_active:
                    auth_login(request, user)
                    return redirect('estoques:menus')
                else:
                    messages.error(request, 'CPF ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'autenticacao/login_funcionario.html', {'form': form})


def esqueceu_senha(request):
    if request.method == 'POST':
        form = EsqueceuSenhaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome_completo']
            cpf = form.cleaned_data['cpf']
            nascimento = form.cleaned_data['data_nascimento']
            nova_senha = form.cleaned_data['nova_senha']

            try:
                cliente = Cliente.objects.get(
                    nome_completo__iexact=nome.strip(),
                    cpf=cpf,
                    data_nascimento=nascimento
                )
                usuario = cliente.user
                usuario.set_password(nova_senha)
                usuario.save()

                messages.success(request, "Senha redefinida com sucesso. Faça login com a nova senha.")
                return redirect("autenticacao:login")

            except Cliente.DoesNotExist:
                messages.error(request, "Dados não encontrados. Verifique e tente novamente.")
    else:
        form = EsqueceuSenhaForm()

    return render(request, 'autenticacao/esqueceu_senha.html', {'form': form})

