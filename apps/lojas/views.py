from django.shortcuts import render, redirect
from django.contrib import messages

from apps.contatos.forms import ContatoForm
from apps.enderecos.forms import EnderecoForm
from apps.lojas.domain import LojaDomain
from apps.lojas.forms import LojaFormSet, LojaForm
from apps.lojas.models import Loja, LojaContato


def listar_lojas(request):
    nome = request.GET.get('nome', '')
    status = request.GET.get('status', '')

    lojas = Loja.objects.all()

    if nome:
        lojas = lojas.filter(nome__icontains=nome)

    if status == 'ativo':
        lojas = lojas.filter(status=True)
    elif status == 'inativo':
        lojas = lojas.filter(status=False)

    context = {
        'lojas': lojas,
        'filtro_nome': nome,
        'filtro_status': status,
    }
    return render(request, 'loja/listar_lojas.html', context)


def adicionar_loja(request):
    if request.method == 'POST':
        formset = LojaFormSet(request.POST, prefix='loja')
        endereco_form = EnderecoForm(request.POST, prefix='endereco')
        contato_form = ContatoForm(request.POST, prefix='contato')

        if formset.is_valid() and endereco_form.is_valid() and contato_form.is_valid():
            endereco = endereco_form.save()
            contato = contato_form.save()

            for form in formset:
                if form.cleaned_data:
                    loja = form.save(commit=False)
                    loja.endereco = endereco
                    loja.save()
                    LojaContato.objects.get_or_create(loja=loja, contato=contato)

            messages.success(request, 'Loja adicionada com sucesso!')
            return redirect('lojas:listar_lojas')

    else:
        formset = LojaFormSet(queryset=Loja.objects.none(), prefix='loja')
        endereco_form = EnderecoForm(prefix='endereco')
        contato_form = ContatoForm(prefix='contato')

    context = {
        'formset': formset,
        'endereco_form': endereco_form,
        'contato_form': contato_form
    }

    return render(request, 'loja/adicionar_loja.html', context)
def editar_loja(request, id_loja):
    domain = LojaDomain.instance_by_loja(id_loja)
    loja = domain.get_loja()

    endereco = loja.endereco or None
    loja_contato = LojaContato.objects.filter(loja=loja).first()
    contato = loja_contato.contato if loja_contato else None

    if request.method == 'POST':
        loja_form = LojaForm(request.POST, instance=loja)
        endereco_form = EnderecoForm(request.POST, instance=endereco, prefix='endereco')
        contato_form = ContatoForm(request.POST, instance=contato, prefix='contato')

        if loja_form.is_valid() and endereco_form.is_valid() and contato_form.is_valid():
            endereco = endereco_form.save()
            contato = contato_form.save()

            loja = loja_form.save(commit=False)
            loja.endereco = endereco
            loja.save()

            if loja_contato:
                loja_contato.contato = contato
                loja_contato.save()
            else:
                LojaContato.objects.create(loja=loja, contato=contato)

            messages.success(request, 'Loja atualizada com sucesso!')
            return redirect('lojas:listar_lojas')

    else:
        loja_form = LojaForm(instance=loja)
        endereco_form = EnderecoForm(instance=endereco, prefix='endereco')
        contato_form = ContatoForm(instance=contato, prefix='contato')

    context = {
        'loja_form': loja_form,
        'endereco_form': endereco_form,
        'contato_form': contato_form,
        'loja_id': loja.id,
    }

    return render(request, 'loja/editar_loja.html', context)