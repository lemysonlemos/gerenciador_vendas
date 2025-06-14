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
from apps.vinculos.models import Vinculo


def listar_vinculos(request):
    cpf = request.GET.get('cpf', '').strip()
    nome = request.GET.get('nome', '').strip()
    loja = request.GET.get('loja', '').strip()
    perfil = request.GET.get('perfil', '').strip()
    status = request.GET.get('status', '').strip()

    vinculos = Vinculo.objects.select_related('usuario__cliente', 'loja').all()

    if cpf:
        vinculos = vinculos.filter(usuario__cliente__cpf__icontains=cpf)
    if nome:
        vinculos = vinculos.filter(usuario__cliente__nome_completo__icontains=nome)
    if loja:
        vinculos = vinculos.filter(loja__nome__icontains=loja)
    if perfil != '':
        vinculos = vinculos.filter(perfil=perfil)
    if status != '':
        vinculos = vinculos.filter(status=status)

    context = {
        'vinculos': vinculos,
        'filtro_cpf': cpf,
        'filtro_nome': nome,
        'filtro_loja': loja,
        'filtro_perfil': perfil,
        'filtro_status': status,
        'perfil_choices': Vinculo.StatusVinculo.choices,  # para mostrar no select
        'status_choices': Vinculo.PerfilVinculo.choices,
        'status_choices_full': Vinculo.STATUS_CHOICES,
        'perfil_choices_full': Vinculo.STATUS_PERFIL,
    }
    return render(request, 'vinculo/listar_vinculos.html', context)


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