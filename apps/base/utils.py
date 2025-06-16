import re
from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

from apps.vinculos.models import Vinculo


def digits(txt):
    """
    Keep only digits in txt.

    >>> digits('15-12/1985.')
    >>> '15121985'
    """
    if txt:
        return re.sub(r'\D', '', txt)
    return txt


def is_admin(user):
    if not hasattr(user, 'usuario'):
        return False
    return Vinculo.objects.filter(
        usuario=user.usuario,
        perfil=Vinculo.StatusVinculo.ADMIN,
        status=Vinculo.StatusVinculo.ATIVO
    ).exists()

def is_gerente(user):
    if not hasattr(user, 'usuario'):
        return False
    return Vinculo.objects.filter(
        usuario=user.usuario,
        perfil=Vinculo.PerfilVinculo.GERENTE,
        status=Vinculo.StatusVinculo.ATIVO
    ).exists()


def is_vendedor(user):
    if not hasattr(user, 'usuario'):
        return False
    return Vinculo.objects.filter(
        usuario=user.usuario,
        perfil=Vinculo.PerfilVinculo.VENDEDOR,
        status=Vinculo.StatusVinculo.ATIVO
    ).exists()


def perfil_requerido(*perfis_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect('autenticacao:login')  # ou seu nome de URL

            if not hasattr(user, 'usuario'):
                return redirect('autenticacao:login')

            if not Vinculo.objects.filter(
                usuario=user.usuario,
                perfil__in=perfis_permitidos,
                status=Vinculo.StatusVinculo.ATIVO
            ).exists():
                return redirect('base:acesso_negado')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator