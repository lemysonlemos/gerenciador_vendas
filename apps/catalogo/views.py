from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.catalogo.domain import ItemDomain, ItemFabricanteDomain
from apps.catalogo.forms import ItemForm, ItemFabricanteFormSet, ItemFabricanteForm, ItemFormSet, FabricanteFormSet, \
    FabricanteForm
from apps.catalogo.models import Item, ItemFabricante, Fabricante


def listar_catalogo(request):
    # Recupera todos os nomes únicos de itens ativos
    nomes_das_abas = (
        Item.objects.filter(ativo=True)
        .values_list('nome', flat=True)
        .distinct()
    )

    # Recebe filtros do request GET
    filtro_fabricante = request.GET.get('fabricante', '')
    filtro_tamanho = request.GET.get('tamanho', '')
    filtro_preco_min = request.GET.get('preco_min', '')
    filtro_preco_max = request.GET.get('preco_max', '')

    abas_com_fabricantes = []

    for nome in nomes_das_abas:
        itens_com_mesmo_nome = Item.objects.filter(nome=nome, ativo=True)

        item_fabricantes = ItemFabricante.objects.filter(item__in=itens_com_mesmo_nome).select_related('fabricante')

        # Aplica os filtros se forem informados
        if filtro_fabricante:
            item_fabricantes = item_fabricantes.filter(fabricante__nome__icontains=filtro_fabricante)
        if filtro_tamanho:
            item_fabricantes = item_fabricantes.filter(tamanho_calcado__icontains=filtro_tamanho)
        if filtro_preco_min:
            try:
                preco_min = float(filtro_preco_min)
                item_fabricantes = item_fabricantes.filter(preco__gte=preco_min)
            except ValueError:
                pass
        if filtro_preco_max:
            try:
                preco_max = float(filtro_preco_max)
                item_fabricantes = item_fabricantes.filter(preco__lte=preco_max)
            except ValueError:
                pass

        abas_com_fabricantes.append({
            'nome_aba': nome,
            'fabricantes': item_fabricantes
        })

    contexto = {
        'abas_com_fabricantes': abas_com_fabricantes,
        'filtros': {
            'fabricante': filtro_fabricante,
            'tamanho': filtro_tamanho,
            'preco_min': filtro_preco_min,
            'preco_max': filtro_preco_max,
        }
    }
    return render(request, 'catalogo/listar_catalogo.html', contexto)

def listar_catalogo_gestao(request):
    # Recupera todos os nomes únicos de itens ativos
    nomes_das_abas = (
        Item.objects.filter(ativo=True)
        .values_list('nome', flat=True)
        .distinct()
    )

    # Recebe filtros do request GET
    filtro_fabricante = request.GET.get('fabricante', '')
    filtro_tamanho = request.GET.get('tamanho', '')
    filtro_preco_min = request.GET.get('preco_min', '')
    filtro_preco_max = request.GET.get('preco_max', '')

    abas_com_fabricantes = []

    for nome in nomes_das_abas:
        itens_com_mesmo_nome = Item.objects.filter(nome=nome, ativo=True)

        item_fabricantes = ItemFabricante.objects.filter(item__in=itens_com_mesmo_nome).select_related('fabricante')

        # Aplica os filtros se forem informados
        if filtro_fabricante:
            item_fabricantes = item_fabricantes.filter(fabricante__nome__icontains=filtro_fabricante)
        if filtro_tamanho:
            item_fabricantes = item_fabricantes.filter(tamanho_calcado__icontains=filtro_tamanho)
        if filtro_preco_min:
            try:
                preco_min = float(filtro_preco_min)
                item_fabricantes = item_fabricantes.filter(preco__gte=preco_min)
            except ValueError:
                pass
        if filtro_preco_max:
            try:
                preco_max = float(filtro_preco_max)
                item_fabricantes = item_fabricantes.filter(preco__lte=preco_max)
            except ValueError:
                pass

        abas_com_fabricantes.append({
            'nome_aba': nome,
            'fabricantes': item_fabricantes
        })

    contexto = {
        'abas_com_fabricantes': abas_com_fabricantes,
        'filtros': {
            'fabricante': filtro_fabricante,
            'tamanho': filtro_tamanho,
            'preco_min': filtro_preco_min,
            'preco_max': filtro_preco_max,
        }
    }
    return render(request, 'catalogo/listar_catalogo_gestao.html', contexto)

def adicionar_catalogo(request):
    if request.method == 'POST':
        formset = ItemFabricanteFormSet(request.POST)

        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, "Item e fabricantes adicionados com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        formset = ItemFabricanteFormSet(queryset=ItemFabricante.objects.none())

    context = {
        'formset': formset,
    }
    return render(request, 'catalogo/adicionar_catalogo.html', context)


def editar_catalogo(request, id_item_fabricante):

    domain = ItemFabricanteDomain.instance_by_itemfabricante(id_item_fabricante)
    queryset = domain.get_item_fabricante()

    if request.method == 'POST':
        form = ItemFabricanteForm(request.POST, instance=queryset)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Item e fabricantes adicionados com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        form = ItemFabricanteForm(instance=queryset)

    context = {
        'form': form,
    }
    return render(request, 'catalogo/editar_catalogo.html', context)


def adicionar_item(request):
    if request.method == 'POST':
        formset = ItemFormSet(request.POST)

        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, "Item com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        formset = ItemFormSet(queryset=Item.objects.none())

    context = {
        'formset': formset,
    }
    return render(request, 'catalogo/adicionar_item.html', context)


def editar_item(request, id_item_fabricante):

    domain = ItemFabricanteDomain.instance_by_itemfabricante(id_item_fabricante)
    queryset = domain.get_item()

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=queryset)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Item e fabricantes adicionados com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        form = ItemForm(instance=queryset)

    context = {
        'form': form,
    }
    return render(request, 'catalogo/editar_item.html', context)


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


def editar_fabricante(request, id_item_fabricante):

    domain = ItemFabricanteDomain.instance_by_itemfabricante(id_item_fabricante)
    queryset = domain.get_fabricante()

    if request.method == 'POST':
        form = FabricanteForm(request.POST, instance=queryset)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Item e fabricantes adicionados com sucesso.")
                    return redirect('catalogo:listar_catalogo_gestao')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao salvar: {e}")
    else:
        form = FabricanteForm(instance=queryset)

    context = {
        'form': form,
    }
    return render(request, 'catalogo/editar_fabricante.html', context)