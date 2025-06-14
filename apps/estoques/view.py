from django.shortcuts import render, redirect, reverse

from apps.estoques.domain import EstoqueDomain
from apps.estoques.forms import EstoqueFormSet, EstoqueForm
from apps.estoques.models import Estoque


def menus(request):
    user = request.user
    return render(request, 'estoque/menus.html')


def listar_estoque(request):
    estoques = Estoque.objects.select_related(
        'catalogo__item', 'catalogo__fabricante', 'loja'
    )

    # Filtros GET
    qtd_min = request.GET.get('qtd_min')
    loja_id = request.GET.get('loja')
    item_id = request.GET.get('item')
    fabricante_id = request.GET.get('fabricante')
    tamanho = request.GET.get('tamanho')
    preco_max = request.GET.get('preco_max')

    if qtd_min:
        estoques = estoques.filter(qtd_estoque__gte=qtd_min)

    if loja_id:
        estoques = estoques.filter(loja_id=loja_id)

    if item_id:
        estoques = estoques.filter(catalogo__item_id=item_id)

    if fabricante_id:
        estoques = estoques.filter(catalogo__fabricante_id=fabricante_id)

    if tamanho:
        estoques = estoques.filter(catalogo__tamanho_calcado__icontains=tamanho)

    if preco_max:
        estoques = estoques.filter(catalogo__preco__lte=preco_max)

    context = {
        'estoques': estoques,
        'request': request,
    }
    return render(request, 'estoque/listar_estoque.html', context)


def adicionar_estoque(request):
    if request.method == 'POST':
        formset = EstoqueFormSet(request.POST, queryset=Estoque.objects.none())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    catalogo = form.cleaned_data['catalogo']
                    loja = form.cleaned_data['loja']
                    if EstoqueDomain.estoque_existe(catalogo, loja):
                        form.add_error(None,
                                       "Já existe estoque com este catálogo e loja. Para alterar, utilize a edição.")
                    else:
                        formset.save()
            return redirect(reverse('estoques:listar_estoque'))
    else:
        formset = EstoqueFormSet(queryset=Estoque.objects.none())

    return render(request, 'estoque/adicionar_estoque.html', {'formset': formset})


def editar_estoque(request, id_estoque):
    domain = EstoqueDomain.insstance_by_estoque(id_estoque)
    estoque = domain.get_estoque()
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return redirect(reverse('estoques:listar_estoque'))
    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'estoque/editar_estoque.html', {'form': form})