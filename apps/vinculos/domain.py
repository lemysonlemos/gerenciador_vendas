from django.db import transaction

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

    def get_vinculo(self):
        return Vinculo.objects.get(id=self.vinculo.id)


    @transaction.atomic
    def salvar(self, user) -> Vinculo:
        try:
            self.vinculo.usuario = user
            self.vinculo.save()
            return self.vinculo
        except (VinculoExisteException,) as e:
            raise e
        except Exception:
            raise VinculoErroGenericoException
