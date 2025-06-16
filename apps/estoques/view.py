from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, reverse

from apps.base.utils import is_admin, is_vendedor, perfil_requerido
from apps.estoques.domain import EstoqueFiltroDomain, EstoqueDomain
from apps.estoques.forms import EstoqueFormSet, EstoqueForm
from apps.estoques.models import Estoque
from apps.vinculos.domain import VinculoDomain
from apps.vinculos.models import Vinculo


def menus(request):
    user = request.user.usuario
    context = {'user': user}
    return render(request, 'estoque/menus.html', context)


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.VENDEDOR, Vinculo.PerfilVinculo.ADMIN)
def listar_estoque(request):

    usuario = request.user.usuario.id
    vinculo_domain = VinculoDomain.new_instance_by_id(usuario)

    filtro_fabricante = request.GET.get('fabricante', '')
    filtro_tamanho = request.GET.get('tamanho', '')
    filtro_preco_min = request.GET.get('preco_min', '')
    filtro_preco_max = request.GET.get('preco_max', '')
    lojas = vinculo_domain.filtro_loja()

    domain = EstoqueFiltroDomain(
        lojas,
        filtro_fabricante=filtro_fabricante,
        filtro_tamanho=filtro_tamanho,
        filtro_preco_min=filtro_preco_min,
        filtro_preco_max=filtro_preco_max,
    )

    estoques = domain.listar_estoques_por_aba()

    context = {
        'estoques': estoques,
        'request': request,
    }
    return render(request, 'estoque/listar_estoque.html', context)


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.ADMIN)
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


@perfil_requerido(Vinculo.PerfilVinculo.GERENTE, Vinculo.PerfilVinculo.ADMIN)
def editar_estoque(request, id_estoque):
    domain = EstoqueDomain.instance_by_estoque(id_estoque)
    estoque = domain.get_estoque()
    if request.method == 'POST':
        if 'excluir' in request.POST:
            estoque.delete()
            messages.success(request, "Exclusão realizada com sucesso.")
            return redirect(reverse('estoques:listar_estoque'))

        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return redirect(reverse('estoques:listar_estoque'))
    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'estoque/editar_estoque.html', {'form': form})