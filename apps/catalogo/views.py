from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.base.utils import is_admin, is_vendedor
from apps.catalogo.domain import ItemDomain, ItemFabricanteDomain
from apps.catalogo.forms import ItemForm, ItemFabricanteFormSet, ItemFabricanteForm, ItemFormSet, FabricanteFormSet, \
    FabricanteForm
from apps.catalogo.models import Item, ItemFabricante, Fabricante
from apps.estoques.domain import EstoqueFiltroDomain
from apps.estoques.models import Estoque


def listar_catalogo(request):
    filtro_fabricante = request.GET.get('fabricante', '')
    filtro_tamanho = request.GET.get('tamanho', '')
    filtro_preco_min = request.GET.get('preco_min', '')
    filtro_preco_max = request.GET.get('preco_max', '')

    filtro_domain = EstoqueFiltroDomain(
        filtro_fabricante=filtro_fabricante,
        filtro_tamanho=filtro_tamanho,
        filtro_preco_min=filtro_preco_min,
        filtro_preco_max=filtro_preco_max
    )

    abas_com_estoques = filtro_domain.listar_estoques_por_aba()

    contexto = {
        'abas_com_estoques': abas_com_estoques,
        'filtros': {
            'fabricante': filtro_fabricante,
            'tamanho': filtro_tamanho,
            'preco_min': filtro_preco_min,
            'preco_max': filtro_preco_max,
        }
    }
    return render(request, 'catalogo/listar_catalogo.html', contexto)


@user_passes_test(is_vendedor)
def listar_catalogo_gestao(request):
    filtro_fabricante = request.GET.get('fabricante', '')
    filtro_tamanho = request.GET.get('tamanho', '')
    filtro_preco_min = request.GET.get('preco_min', '')
    filtro_preco_max = request.GET.get('preco_max', '')

    filtro_domain = EstoqueFiltroDomain(
        filtro_fabricante=filtro_fabricante,
        filtro_tamanho=filtro_tamanho,
        filtro_preco_min=filtro_preco_min,
        filtro_preco_max=filtro_preco_max
    )

    abas_com_estoques = filtro_domain.listar_estoques_por_aba()

    contexto = {
        'abas_com_estoques': abas_com_estoques,
        'filtros': {
            'fabricante': filtro_fabricante,
            'tamanho': filtro_tamanho,
            'preco_min': filtro_preco_min,
            'preco_max': filtro_preco_max,
        }
    }
    return render(request, 'catalogo/listar_catalogo_gestao.html', contexto)


@user_passes_test(is_admin)
@permission_required('catalogo.', raise_exception=True)
def adicionar_catalogo(request):
    if request.method == 'POST':
        formset = ItemFabricanteFormSet(request.POST, request.FILES)

        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, "Catálogo adicionados com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        formset = ItemFabricanteFormSet(queryset=ItemFabricante.objects.none())

    context = {
        'formset': formset,
    }
    return render(request, 'catalogo/adicionar_catalogo.html', context)


@user_passes_test(is_admin)
def editar_catalogo(request, id_item_fabricante):

    domain = ItemFabricanteDomain.instance_by_itemfabricante(id_item_fabricante)
    queryset = domain.get_item_fabricante()

    if request.method == 'POST':
        form = ItemFabricanteForm(request.POST, request.FILES, instance=queryset)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Catálogo editado com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        form = ItemFabricanteForm(instance=queryset)

    context = {
        'form': form,
    }
    return render(request, 'catalogo/editar_catalogo.html', context)


@user_passes_test(is_admin)
def adicionar_item(request):
    if request.method == 'POST':
        formset = ItemFormSet(request.POST)

        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, "Item adicionado com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        formset = ItemFormSet(queryset=Item.objects.none())

    context = {
        'formset': formset,
    }
    return render(request, 'catalogo/adicionar_item.html', context)


@user_passes_test(is_admin)
def editar_item(request, id_item_fabricante):

    domain = ItemFabricanteDomain.instance_by_itemfabricante(id_item_fabricante)
    queryset = domain.get_item()

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=queryset)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Item editado com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        form = ItemForm(instance=queryset)

    context = {
        'form': form,
    }
    return render(request, 'catalogo/editar_item.html', context)


@user_passes_test(is_admin)
def adicionar_fabricante(request):
    if request.method == 'POST':
        formset = FabricanteFormSet(request.POST)

        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, "Fabricantes adicionados com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        formset = FabricanteFormSet(queryset=Fabricante.objects.none())

    context = {
        'formset': formset,
    }
    return render(request, 'catalogo/adicionar_fabricante.html', context)


@user_passes_test(is_admin)
def editar_fabricante(request, id_item_fabricante):

    domain = ItemFabricanteDomain.instance_by_itemfabricante(id_item_fabricante)
    queryset = domain.get_fabricante()

    if request.method == 'POST':
        form = FabricanteForm(request.POST, instance=queryset)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Fabricante adicionado com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        form = FabricanteForm(instance=queryset)

    context = {
        'form': form,
    }
    return render(request, 'catalogo/editar_fabricante.html', context)