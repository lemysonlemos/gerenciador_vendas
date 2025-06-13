from django.shortcuts import render

from apps.catalogo.domain import ItemDomain
from apps.catalogo.models import Item, ItemFabricante


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
            item_fabricantes = item_fabricantes.filter(tamanho_calçado__icontains=filtro_tamanho)
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
