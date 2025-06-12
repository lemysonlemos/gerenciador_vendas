from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import safestring
from django.urls import reverse_lazy, reverse

from apps import cliente
from apps.autenticacao.models import UsuarioBase
from apps.cliente.domain import salvar_cliente_com_formsets
from apps.cliente.forms import CadastrarClienteForm, AnexoClienteForm, CpfForm
from apps.cliente.models import Cliente, ClienteEndereco, ClienteContato
from apps.contatos.forms import ContatoFormSet
from apps.contatos.models import Contato
from apps.enderecos.forms import EnderecoFormSet
from apps.enderecos.models import Endereco



def cadastro(request):
    if request.method == 'POST':
        form = CadastrarClienteForm(request.POST, request.FILES)
        contato_formset = ContatoFormSet(request.POST, prefix='contato')
        endereco_formset = EnderecoFormSet(request.POST, prefix='endereco')
        form_anexo = AnexoClienteForm(request.POST, request.FILES)

        if all([form.is_valid(), contato_formset.is_valid(), endereco_formset.is_valid(), form_anexo.is_valid()]):
            try:
                with transaction.atomic():
                    salvar_cliente_com_formsets(
                        form=form,
                        contato_formset=contato_formset,
                        endereco_formset=endereco_formset,
                        form_anexo=form_anexo
                    )
                    messages.success(request, "Cadastro realizado com sucesso!")
                    return redirect('pos-autocadastro')  # Redireciona para página de confirmação
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar os dados: {e}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CadastrarClienteForm()
        contato_formset = ContatoFormSet(prefix='contato')
        endereco_formset = EnderecoFormSet(prefix='endereco')
        form_anexo = AnexoClienteForm()
    context = {
            'form': form,
            'contato_formset': contato_formset,
            'endereco_formset': endereco_formset,
            'form_anexo': form_anexo,
        }
    return render(request,'cliente/cadastro.html', context)

