from apps.estoques.models import Estoque


class EstoqueDomain:
    def __init__(self, estoque):
        self.estoque = estoque

    @staticmethod
    def instance_by_estoque(id_estoque: int):
        estoque = Estoque.objects.get(id=id_estoque)
        return EstoqueDomain(estoque=estoque)

    def get_estoque(self):
        return Estoque.objects.get(id=self.estoque.id)
    @staticmethod
    def estoque_existe(catalogo, loja) -> bool:
        return Estoque.objects.filter(catalogo=catalogo, loja=loja).exists()


class EstoqueFiltroDomain:
    def __init__(self, lojas, filtro_fabricante='', filtro_tamanho='', filtro_preco_min='', filtro_preco_max=''):
        self.filtro_fabricante = filtro_fabricante
        self.filtro_tamanho = filtro_tamanho
        self.filtro_preco_min = filtro_preco_min
        self.filtro_preco_max = filtro_preco_max
        self.lojas = lojas

    def listar_estoques_por_aba(self):
        nomes_das_abas = (
            Estoque.objects.filter(catalogo__item__ativo=True, loja__in=self.lojas)
            .values_list('catalogo__item__nome', flat=True)
            .distinct()
        ).order_by('catalogo__item__nome')

        abas_com_estoques = []

        for nome in nomes_das_abas:
            estoques = Estoque.objects.filter(catalogo__item__nome=nome, catalogo__item__ativo=True)

            if self.filtro_fabricante:
                estoques = estoques.filter(catalogo__fabricante__nome__icontains=self.filtro_fabricante)
            if self.filtro_tamanho:
                estoques = estoques.filter(catalogo__tamanho_calcado__icontains=self.filtro_tamanho)
            if self.filtro_preco_min:
                try:
                    preco_min = float(self.filtro_preco_min)
                    estoques = estoques.filter(catalogo__preco__gte=preco_min)
                except ValueError:
                    pass
            if self.filtro_preco_max:
                try:
                    preco_max = float(self.filtro_preco_max)
                    estoques = estoques.filter(catalogo__preco__lte=preco_max)
                except ValueError:
                    pass

            abas_com_estoques.append({
                'nome_aba': nome,
                'estoques': estoques
            })

        return abas_com_estoques


class EstoqueFiltroClienteDomain:
    def __init__(self, filtro_fabricante='', filtro_tamanho='', filtro_preco_min='', filtro_preco_max='',
                 filtro_loja=''):
        self.filtro_fabricante = filtro_fabricante
        self.filtro_tamanho = filtro_tamanho
        self.filtro_preco_min = filtro_preco_min
        self.filtro_preco_max = filtro_preco_max

    def listar_estoques_por_aba(self):
        nomes_das_abas = (
            Estoque.objects.filter(catalogo__item__ativo=True)
            .values_list('catalogo__item__nome', flat=True)
            .distinct()
        )

        abas_com_estoques = []

        for nome in nomes_das_abas:
            estoques = Estoque.objects.filter(catalogo__item__nome=nome, catalogo__item__ativo=True)

            if self.filtro_fabricante:
                estoques = estoques.filter(catalogo__fabricante__nome__icontains=self.filtro_fabricante)
            if self.filtro_tamanho:
                estoques = estoques.filter(catalogo__tamanho_calcado__icontains=self.filtro_tamanho)
            if self.filtro_preco_min:
                try:
                    preco_min = float(self.filtro_preco_min)
                    estoques = estoques.filter(catalogo__preco__gte=preco_min)
                except ValueError:
                    pass
            if self.filtro_preco_max:
                try:
                    preco_max = float(self.filtro_preco_max)
                    estoques = estoques.filter(catalogo__preco__lte=preco_max)
                except ValueError:
                    pass

            abas_com_estoques.append({
                'nome_aba': nome,
                'estoques': estoques
            })

        return abas_com_estoques
