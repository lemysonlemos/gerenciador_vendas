import re

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


def is_vendedor(user):
    if not hasattr(user, 'usuario'):
        return False
    return Vinculo.objects.filter(
        usuario=user.usuario,
        perfil__in=[Vinculo.PerfilVinculo.ADMIN, Vinculo.PerfilVinculo.VENDEDOR],
        status=Vinculo.StatusVinculo.ATIVO
    ).exists()