from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import safestring
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe

from apps import cliente
from apps.autenticacao.models import UsuarioBase
from apps.base.formsets import FormSetFactory
from apps.cliente.dataclasses import DadosClienteDTO
from apps.cliente.domain import ClienteDomain
from apps.cliente.exceptions import ClienteErroGenericoException
from apps.cliente.forms import CadastrarClienteForm, AnexoClienteForm, CpfForm, ClienteForm
from apps.cliente.models import Cliente, ClienteEndereco, ClienteContato
from apps.contatos.forms import ContatoFormSet, ContatoForm
from apps.contatos.models import Contato
from apps.enderecos.forms import EnderecoFormSet, EnderecoForm
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
                    enderecos_mais = endereco_formset.save()
                    contatos_mais = contato_formset.save()
                    cliente = form.instance
                    cliente.endereco = enderecos_mais[0]
                    cliente.contato = contatos_mais[0] if contatos_mais else None
                    cliente = form.save()

                    for endereco in enderecos_mais:
                        ClienteEndereco.objects.create(
                            cliente=cliente,
                            endereco=endereco,
                        )
                    for contato in contatos_mais:
                        ClienteContato.objects.create(
                            cliente=cliente,
                            contato=contato,
                        )

                    cliente.save()

                    if form_anexo.cleaned_data.get("arquivo"):
                        anexo = form_anexo.save(commit=False)
                        anexo.cliente = cliente
                        anexo.save()

                    messages.success(request, "Cadastro realizado com sucesso!")
                    return redirect('autenticacao:login')  # Redireciona para página de confirmação
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar os dados: {e}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CadastrarClienteForm()
        contato_formset = ContatoFormSet(queryset=Contato.objects.none(), prefix='contato')
        endereco_formset = EnderecoFormSet(queryset=Endereco.objects.none(), prefix='endereco')
        form_anexo = AnexoClienteForm()
    context = {
            'form': form,
            'contato_formset': contato_formset,
            'endereco_formset': endereco_formset,
            'form_anexo': form_anexo,
        }
    return render(request,'cliente/cadastro.html', context)


@login_required(login_url=reverse_lazy('autenticacao:login'))
def painel(request):

    cliente = ClienteDomain.insstance_by_cliente(request.user.cliente.id)

    context = {
        'cliente_nome': cliente.cliente.nome_completo,
    }
    return render(request, 'cliente/painel.html', context)


@login_required(login_url=reverse_lazy('autenticacao:login'))
def perfil(request):
    domain = ClienteDomain(request.user.cliente)

    form_cliente = ClienteForm(
        request.POST or None,
        request.FILES or None,
        instance=domain.cliente
    )
    formset_contato = FormSetFactory(
        request.POST or None,
        model=Contato,
        prefix='contato',
        form=ContatoForm, queryset=domain.get_contatos_cliente(), extra=1, min_num=0,
        max_num=3, validate_min=True, can_delete=True
    ).get_formset()
    formset_endereco = FormSetFactory(
        request.POST or None, model=Endereco, prefix='endereco',
        form=EnderecoForm, queryset=domain.get_enderecos_cliente(), extra=0, min_num=1,
        max_num=3, validate_min=True, can_delete=True
    ).get_formset()

    if request.POST:
        try:
            if all([form_cliente.is_valid() and formset_contato.is_valid() and formset_endereco.is_valid()]):
                cliente = form_cliente.save(commit=False)
                enderecos = formset_endereco.save(commit=False)
                enderecos_delete = formset_endereco.deleted_objects
                contatos = formset_contato.save(commit=False)
                contatos_delete = formset_contato.deleted_objects
                dados_cliente = DadosClienteDTO(
                    enderecos=enderecos,
                    contatos=contatos,
                    request=request,
                    enderecos_delete=enderecos_delete,
                    contatos_delete=contatos_delete
                )
                domain = ClienteDomain(
                    cliente=cliente,
                )
                domain.editar(dados_cliente)
                messages.success(request, mark_safe('Perfil atualizado com sucesso.'))
                return redirect('cliente:painel')
            else:
                raise ClienteErroGenericoException()
        except Exception as e:
            messages.error(request, mark_safe(str(e)))
    context = {
        'form_cliente': form_cliente,
        'formset_contato': formset_contato,
        'formset_endereco': formset_endereco,
    }
    return render(request, 'cliente/perfil.html', context)

