from apps.lojas.models import Loja


class LojaDomain:
    def __init__(self, loja):
        self.loja = loja


    @staticmethod
    def instance_by_loja(id_loja: int):
        loja = Loja.objects.get(id=id_loja)
        return LojaDomain(loja=loja)

    def get_loja(self):
        return Loja.objects.get(id=self.loja.id)