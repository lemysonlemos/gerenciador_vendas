from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from apps.base.utils import is_vendedor, perfil_requerido
from apps.compras.domain import ComprasDomain, ComprasFiltroDomain, ComprasFiltroClienteDomain
from apps.compras.forms import CompraForm, CompraGestaoForm
from apps.compras.models import Compra
from apps.estoques.domain import EstoqueDomain
from apps.vinculos.domain import VinculoDomain
from apps.vinculos.models import Vinculo


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.VENDEDOR, Vinculo.PerfilVinculo.ADMIN)
def listar_compras(request):
    usuario = request.user.usuario.id
    vinculo_domain = VinculoDomain.new_instance_by_id(usuario)
    lojas = vinculo_domain.filtro_loja()

    filtro_cliente = request.GET.get("cliente", "")
    filtro_item = request.GET.get("item", "")
    filtro_vendedor = request.GET.get("vendedor", "")
    filtro_fabricante = request.GET.get("fabricante", "")
    filtro_loja = request.GET.get("loja", "")

    domain = ComprasFiltroDomain(
        lojas,
        filtro_cliente=filtro_cliente,
        filtro_vendedor=filtro_vendedor,
        filtro_item=filtro_item,
        filtro_fabricante=filtro_fabricante,
        filtro_loja=filtro_loja,
    )
    compras = domain.filter_compras()

    context = {
        'compras': compras,
        'filtro_cliente': filtro_cliente,
        'filtro_item': filtro_item,
        'filtro_loja': filtro_loja,
        'filtro_vendedor': filtro_vendedor,
        'filtro_fabricante': filtro_fabricante,
    }

    return render(request, 'compras/listar_compras_gestao.html', context)


@login_required(login_url=reverse_lazy('autenticacao:login'))
def listar_compras_cliente(request):
    filtro_item = request.GET.get("item", "")
    filtro_loja = request.GET.get("loja", "")
    filtro_fabricante = request.GET.get("fabricante", "")

    cliente = request.user.cliente

    domain = ComprasFiltroClienteDomain(
        cliente,
        filtro_item=filtro_item,
        filtro_loja=filtro_loja,
        filtro_fabricante=filtro_fabricante
    )
    compras = domain.filter_compras()

    context = {
        'compras': compras,
        'filtro_item': filtro_item,
        'filtro_loja': filtro_loja,
        'filtro_fabricante': filtro_fabricante,
    }

    return render(request, 'compras/listar_compras.html', context)


def compra_cliente(request):
    cliente = request.user.cliente
    id_estoque = request.GET.get('estoque_id')

    estoque = EstoqueDomain.instance_by_estoque(id_estoque).estoque

    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            qtd = form.cleaned_data['qtd_compra']
            pagamento = form.cleaned_data['pagamento']
            compra = Compra(
                cliente=cliente,
                estoque=estoque,
                catalogo=estoque.catalogo,
                loja=estoque.loja,
                qtd_compra=qtd,
                pagamento=pagamento,
                status_compra_online=True,
                compra_finalizada=True,
                cancelar_compra=False,
            )
            try:
                with transaction.atomic():
                    compra.save()
                messages.success(request, "Compra realizada com sucesso!")
                return redirect('compras:listar_compras_cliente')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = CompraForm(initial={'estoque_id': estoque.id})

    context = {
        'form': form,
        'estoque': estoque,
    }
    return render(request, 'compras/compra_cliente.html', context)


def compra_cancelada(request, id_compra):

    domain = ComprasDomain.instance_by_compras(id_compra)
    compra = domain.compra

    if not compra.cancelar_compra:
        compra.cancelar()
        messages.success(request, "Compra cancelada com sucesso.")
    else:
        messages.warning(request, "Não é possível cancelar esta compra.")

    return redirect('compras:listar_compras')


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.VENDEDOR, Vinculo.PerfilVinculo.ADMIN)
def compra_vendedor(request, id_estoque):
    vendedor = request.user.usuario.vinculos.first()

    estoque = EstoqueDomain.instance_by_estoque(id_estoque).estoque

    if request.method == 'POST':
        form = CompraGestaoForm(request.POST)
        if form.is_valid():
            qtd = form.cleaned_data['qtd_compra']
            pagamento = form.cleaned_data['pagamento']
            cliente = form.cleaned_data['cliente']
            compra = Compra(
                cliente=cliente,
                vendedor=vendedor,
                estoque=estoque,
                catalogo=estoque.catalogo,
                loja=estoque.loja,
                qtd_compra=qtd,
                pagamento=pagamento,
                status_compra_online=False,
                compra_finalizada=True,
                cancelar_compra=False,
            )
            try:
                with transaction.atomic():
                    compra.save()
                messages.success(request, "Compra realizada com sucesso!")
                return redirect('compras:listar_compras')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = CompraGestaoForm(initial={'estoque_id': estoque.id})

    context = {
        'form': form,
        'estoque': estoque,
    }
    return render(request, 'compras/compra_vendedor.html', context)


