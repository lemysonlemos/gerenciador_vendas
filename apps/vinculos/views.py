from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib import messages

from apps.vinculos.domain import VinculoDomain


@login_required
def novo(request):
    if not hasattr(request.user, 'usuario'):
        logout(request)
        return redirect('autenticacao:login')

    form = VinculoForm(request.POST or None)
    if request.POST:
        try:
            if form.is_valid():
                vinculo = form.save(commit=False)
                vinculo.usuario = request.user.usuario
                vinculo_domain = VinculoDomain(vinculo=vinculo)
                vinculo_domain.salvar()
                messages.success(request, mark_safe("Vínculo registrado com sucesso. Aguarde a homologação."))
                return redirect('vinculos:vinculos')
            # else:
            #     raise VinculoErroGenericoException()
        except Exception as e:
            messages.error(request, mark_safe(str(e)))
    return redirect('vinculos:vinculos')