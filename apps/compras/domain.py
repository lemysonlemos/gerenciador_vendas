from apps.compras.models import Compra


class ComprasDomain:
    def __init__(self, compra):
        self.compra = compra

    @staticmethod
    def instance_by_compras(id_compras:int):
        compra = Compra.objects.get(id=id_compras)
        return ComprasDomain(compra=compra)


class ComprasFiltroDomain:
        def __init__(self, lojas, filtro_cliente=None, filtro_vendedor=None, filtro_item=None, filtro_fabricante=None, filtro_loja=None):
            self.filtro_cliente = filtro_cliente
            self.filtro_vendedor = filtro_vendedor
            self.filtro_item = filtro_item
            self.filtro_fabricante = filtro_fabricante
            self.filtro_loja = filtro_loja
            self.lojas = lojas

        def filter_compras(self):
            compras = Compra.objects.filter(loja__in=self.lojas).distinct()
            if self.filtro_cliente:
                compras = compras.filter(cliente__nome_completo__icontains=self.filtro_cliente)
            if self.filtro_vendedor:
                compras = compras.filter(vendedor__nome__icontains=self.filtro_vendedor)
            if self.filtro_item:
                compras = compras.filter(catalogo__item__nome__icontains=self.filtro_item)
            if self.filtro_loja:
                compras = compras.filter(loja__nome__icontains=self.filtro_loja)
            if self.filtro_fabricante:
                compras = compras.filter(catalogo__fabricante__nome__icontains=self.filtro_fabricante)
            return compras.order_by('-id')


class ComprasFiltroClienteDomain:
    def __init__(self, cliente, filtro_vendedor=None, filtro_item=None, filtro_fabricante=None,
                 filtro_loja=None):
        self.cliente = cliente
        self.filtro_vendedor = filtro_vendedor
        self.filtro_item = filtro_item
        self.filtro_fabricante = filtro_fabricante
        self.filtro_loja = filtro_loja

    def filter_compras(self):
        compras = Compra.objects.filter(cliente=self.cliente).distinct()
        if self.filtro_vendedor:
            compras = compras.filter(vendedor__nome__icontains=self.filtro_vendedor)
        if self.filtro_item:
            compras = compras.filter(catalogo__item__nome__icontains=self.filtro_item)
        if self.filtro_loja:
            compras = compras.filter(loja__nome__icontains=self.filtro_loja)
        if self.filtro_fabricante:
            compras = compras.filter(catalogo__fabricante__nome__icontains=self.filtro_fabricante)
        return compras.order_by('-id')
