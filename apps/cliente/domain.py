from apps.cliente.models import AnexoCliente


def salvar_cliente_com_formsets(form, contato_formset, endereco_formset, form_anexo):
    """
    Salva um cidadão e seus contatos, endereços e documento anexo usando os formsets.
    Deve ser usado dentro de uma transação atômica.
    """
    cidadao = form.save()

    contatos = contato_formset.save(commit=False)
    for contato in contatos:
        contato.cidadao = cidadao
        contato.save()

    enderecos = endereco_formset.save(commit=False)
    for endereco in enderecos:
        endereco.cidadao = cidadao
        endereco.save()

    if form_anexo.cleaned_data.get('arquivo'):
        AnexoCliente.objects.get_or_create(
            cidadao=cidadao,
            descricao=form_anexo.cleaned_data.get('descricao'),
            arquivo=form_anexo.cleaned_data.get('arquivo'),
        )

    return cidadao