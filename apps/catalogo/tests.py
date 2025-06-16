from django.test import TestCase
from apps.catalogo.models import Item, Fabricante, ItemFabricante
from django.db import IntegrityError

class ItemModelTest(TestCase):

    def test_criar_item(self):
        item = Item.objects.create(
            nome="Tênis Esportivo teste",
            nome_reduzido="Tênis",
            descricao="Um tênis para corrida teste.",
            ativo=True
        )
        self.assertIsNotNone(item.id)
        self.assertEqual(str(item), "Tênis Esportivo teste")
        self.assertEqual(item.nome_reduzido, "Tênis")
        self.assertEqual(item.descricao, "Um tênis para corrida teste.")

class FabricanteModelTest(TestCase):

    def test_criar_fabricante(self):
        fabricante = Fabricante.objects.create(
            nome="Nike teste",
            nome_reduzido="NK",
            ativo=True
        )
        self.assertIsNotNone(fabricante.id)
        self.assertEqual(str(fabricante), "Nike teste")

class ItemFabricanteModelTest(TestCase):

    def setUp(self):
        self.item = Item.objects.create(nome="Tênis Corrida teste", nome_reduzido="Corrida teste")
        self.fabricante = Fabricante.objects.create(nome="Adidas teste", nome_reduzido="AD")

    def test_criar_relacao_item_fabricante(self):
        relacao = ItemFabricante.objects.create(
            item=self.item,
            fabricante=self.fabricante,
            tamanho_calcado="42",
            preco=299.99
        )
        self.assertIsNotNone(relacao.id)
        self.assertEqual(relacao.item, self.item)
        self.assertEqual(relacao.fabricante, self.fabricante)
        self.assertEqual(relacao.tamanho_calcado, "42")
        self.assertEqual(relacao.preco, 299.99)
        self.assertEqual(
            str(relacao),
            f"{self.item.nome} - {self.fabricante.nome} - 42 - R$299.99"
        )

    def test_unique_together_constraint(self):
        ItemFabricante.objects.create(item=self.item, fabricante=self.fabricante)
        with self.assertRaises(IntegrityError):
            ItemFabricante.objects.create(item=self.item, fabricante=self.fabricante)
