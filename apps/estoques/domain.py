from apps.estoques.models import Estoque


class EstoqueDomain:
    def __init__(self, estoque):
        self.estoque = estoque

    @staticmethod
    def insstance_by_estoque(id_estoque: int):
        estoque = Estoque.objects.get(id=id_estoque)
        return EstoqueDomain(estoque=estoque)

    def get_estoque(self):
        return Estoque.objects.get(id=self.estoque.id)
    @staticmethod
    def estoque_existe(catalogo, loja) -> bool:
        return Estoque.objects.filter(catalogo=catalogo, loja=loja).exists()