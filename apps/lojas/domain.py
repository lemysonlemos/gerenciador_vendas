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


class LojaFiltroDomain:
    def __init__(self, lojas, filtro_nome=None, filtro_status=None):
        self.lojas = lojas
        self.filtro_nome = filtro_nome
        self.filtro_status = filtro_status

    def filter_lojas(self):
        lojas = Loja.objects.filter(loja__in=self.lojas).distinct()

        if self.filtro_nome:
            lojas = lojas.filter(nome__icontains=self.filtro_nome)

        if self.filtro_status == 'ativo':
            lojas = lojas.filter(status=True)
        elif self.filtro_status == 'inativo':
            lojas = lojas.filter(status=False)

        return lojas.order_by('nome')