from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib import messages

from apps.cliente.domain import ClienteDomain
from apps.cliente.forms import CadastrarClienteForm, ClienteForm, CpfForm
from apps.vinculos.domain import VinculoDomain
from apps.vinculos.exception import VinculoErroGenericoException
from apps.vinculos.forms import VinculoForm


def informar_cpf(request):
    if request.POST:
        form = CpfForm(request.POST or None)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            cliente = ClienteDomain.get_busca_cpf(cpf)
            if cliente:
                return redirect('vinculos:novo', id_cliente=cliente.id)
            else:
                return redirect('cliente:cadastro')
    else:
        form = CpfForm()
    context = {
        'form': form,
    }
    return render(request,'vinculo/informar_cpf.html', context)
def novo(request, id_cliente):

    if request.POST:
        form = VinculoForm(request.POST or None)
        try:
            if form.is_valid():
                vinculo = form.save(commit=False)
                vinculo_domain = VinculoDomain(vinculo=vinculo)
                user = vinculo_domain.get_usuario(id_cliente)
                vinculo_domain.salvar(user)
                messages.success(request, mark_safe("Vínculo registrado com sucesso. Aguarde a homologação."))
                return redirect('autenticacao:login_funcionario')
            else:
                raise VinculoErroGenericoException()
        except Exception as e:
            messages.error(request, mark_safe(str(e)))
    else:
        form = VinculoForm()

    context = {
        'form': form,
    }

    return render(request,'vinculo/novo.html', context)