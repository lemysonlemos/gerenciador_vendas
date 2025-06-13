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