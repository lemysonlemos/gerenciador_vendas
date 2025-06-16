from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib import messages

from apps.base.utils import is_admin, is_vendedor, perfil_requerido
from apps.cliente.domain import ClienteDomain
from apps.cliente.forms import CadastrarClienteForm, ClienteForm, CpfForm
from apps.vinculos.domain import VinculoDomain, VinculosFiltroDomain
from apps.vinculos.exception import VinculoErroGenericoException
from apps.vinculos.forms import VinculoForm
from apps.vinculos.models import Vinculo


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.ADMIN)
def listar_vinculos(request):
    usuario = request.user.usuario.id
    vinculo_domain = VinculoDomain.new_instance_by_id(usuario)
    lojas = vinculo_domain.filtro_loja()

    cpf = request.GET.get('cpf', '').strip()
    nome = request.GET.get('nome', '').strip()
    loja = request.GET.get('loja', '').strip()
    perfil = request.GET.get('perfil', '').strip()
    status = request.GET.get('status', '').strip()

    filtro = VinculosFiltroDomain(
        lojas=lojas,
        cpf=cpf,
        nome=nome,
        loja_nome=loja,
        perfil=perfil,
        status=status
    )

    vinculos = filtro.filtrar()

    context = {
        'vinculos': vinculos,
        'filtro_cpf': cpf,
        'filtro_nome': nome,
        'filtro_loja': loja,
        'filtro_perfil': perfil,
        'filtro_status': status,
        'perfil_choices': Vinculo.StatusVinculo.choices,
        'status_choices': Vinculo.PerfilVinculo.choices,
        'status_choices_full': Vinculo.STATUS_CHOICES,
        'perfil_choices_full': Vinculo.STATUS_PERFIL,
    }
    return render(request, 'vinculo/listar_vinculos.html', context)


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.ADMIN)
def adicionar_vinculo(request):
    if request.method == 'POST':
        form = VinculoForm(request.POST)
        if form.is_valid():
            vinculo = form.save()
            messages.success(request, 'Vínculo adicionado com sucesso.')
            return redirect('vinculos:listar_vinculos')
    else:
        form = VinculoForm()

    return render(request, 'vinculo/vinculo_gestao.html', {'form': form, 'titulo': 'Adicionar Vínculo'})


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.ADMIN)
def editar_vinculo(request, vinculo_id):
    domain = VinculoDomain.new_instance_by_id(vinculo_id)
    vinculo = domain.get_vinculo()

    if request.method == 'POST':
        form = VinculoForm(request.POST, instance=vinculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vínculo atualizado com sucesso.')
            return redirect('vinculos:listar_vinculos')
    else:
        form = VinculoForm(instance=vinculo)

    return render(request, 'vinculo/vinculo_gestao.html', {'form': form, 'titulo': 'Editar Vínculo'})