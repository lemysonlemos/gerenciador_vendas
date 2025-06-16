from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.catalogo.models import ItemFabricante
from apps.cliente.models import Cliente
from apps.compras.models import Pagamento, Compra
from apps.estoques.models import Estoque
from apps.lojas.models import Loja
from apps.vinculos.models import Vinculo


class CompraModelTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(nome_completo="João teste")
        self.estoque = Estoque.objects.create(qtd_estoque=10)
        self.catalogo = ItemFabricante.objects.create(item=None, fabricante=None)
        self.loja = Loja.objects.create(nome="Loja 1 - teste 2")
        self.pagamento = Pagamento.objects.create(nome="Cartão teste")
        self.vendedor = Vinculo.objects.create(usuario=None)

    def test_criar_compra_valida_decrementa_estoque(self):
        compra = Compra.objects.create(
            cliente=self.cliente,
            estoque=self.estoque,
            catalogo=self.catalogo,
            loja=self.loja,
            pagamento=self.pagamento,
            vendedor=self.vendedor,
            qtd_compra=5
        )
        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.qtd_estoque, 5)

    def test_criar_compra_com_estoque_insuficiente_lanca_erro(self):
        with self.assertRaises(ValidationError):
            Compra.objects.create(
                cliente=self.cliente,
                estoque=self.estoque,
                catalogo=self.catalogo,
                loja=self.loja,
                pagamento=self.pagamento,
                vendedor=self.vendedor,
                qtd_compra=20
            )

    def test_cancelar_compra_retorna_qtd_para_estoque(self):
        compra = Compra.objects.create(
            cliente=self.cliente,
            estoque=self.estoque,
            catalogo=self.catalogo,
            loja=self.loja,
            pagamento=self.pagamento,
            vendedor=self.vendedor,
            qtd_compra=4
        )
        estoque_original = self.estoque.qtd_estoque

        compra.cancelar()
        self.estoque.refresh_from_db()
        self.assertTrue(compra.cancelar_compra)
        self.assertEqual(self.estoque.qtd_estoque, estoque_original + 4)

    def test_nao_permite_cancelar_duas_vezes(self):
        compra = Compra.objects.create(
            cliente=self.cliente,
            estoque=self.estoque,
            catalogo=self.catalogo,
            loja=self.loja,
            pagamento=self.pagamento,
            vendedor=self.vendedor,
            qtd_compra=2
        )
        compra.cancelar()
        with self.assertRaises(ValidationError):
            compra.cancelar()

    def test_cancelar_compra_sem_estoque_lanca_erro(self):
        compra = Compra.objects.create(
            cliente=self.cliente,
            estoque=None,
            catalogo=self.catalogo,
            loja=self.loja,
            pagamento=self.pagamento,
            vendedor=self.vendedor,
            qtd_compra=2
        )
        with self.assertRaises(ValidationError):
            compra.cancelar()
