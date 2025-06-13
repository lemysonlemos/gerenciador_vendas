from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q

from apps.autenticacao.models import Usuario
from apps.cliente.models import Cliente
from apps.vinculos.exception import VinculoExisteException, VinculoErroGenericoException
from apps.vinculos.models import Vinculo


class VinculoDomain:

    def __init__(self, vinculo: Vinculo):
        self.vinculo = vinculo

    @staticmethod
    def new_instance_by_id(vinculo_id: int) -> 'VinculoDomain':
        vinculo = Vinculo.objects.get(id=vinculo_id)
        return VinculoDomain(
            vinculo=vinculo
        )

    def get_usuario(self, id_cliente):
        cliente = Cliente.objects.get(id=id_cliente)
        return Usuario.objects.get(user=cliente.user)


    @transaction.atomic
    def salvar(self, user) -> Vinculo:
        try:
            # if self.__existe_vinculo_autorizado():
            #     raise VinculoExisteException()
            self.vinculo.usuario = user
            self.vinculo.save()
            return self.vinculo
        except (VinculoExisteException,) as e:
            raise e
        except Exception:
            raise VinculoErroGenericoException

    def __existe_vinculo_autorizado(self) -> bool:
        return Vinculo.objects.filter(
            Q(usuario=self.vinculo.usuario)
            & Q(loja=self.vinculo.loja)
            & Q(perfil=self.vinculo.perfil)
            & ~Q(status=Vinculo.StatusVinculo.INATIVO)
        ).exists()