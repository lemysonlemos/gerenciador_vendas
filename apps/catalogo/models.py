from django.db import models
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel


class Item(BaseModel):
    id = models.AutoField(
        db_column='PK_ITEM',
        primary_key=True
    )
    nome = models.CharField(
        db_column='NO_NOME_ITEM',
        max_length=120
    )
    nome_reduzido = models.CharField(
        db_column='NO_NOME_REDUZIDO',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Nome Reduzido'
    )
    descricao = models.TextField(
        db_column='DS_NOME_ITEM',
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    historico = HistoricalRecords(
        related_name='historico_item'
    )
    ativo = models.BooleanField(
        db_column="ST_ATIVO",
        default=True
    )

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        db_table = 'TB_ITEM'

    def __str__(self):
            return self.nome


class Fabricante(BaseModel):
    id = models.AutoField(
        db_column='PK_FABRICANTE',
        primary_key=True
    )
    nome = models.CharField(
        db_column='NO_FABRICANTE',
        max_length=120,
        unique=True,
        verbose_name='Nome'
    )
    nome_reduzido = models.CharField(
        db_column='NO_NOME_REDUZIDO',
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Nome Reduzido'
    )
    ativo = models.BooleanField(
        default=True,
        db_column='ST_ATIVO'
    )
    historico = HistoricalRecords(
        related_name='historico_fabricante'
    )

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'
        db_table = 'TB_FABRICANTE'

    def __str__(self):
        return self.nome


class ItemFabricante(BaseModel):
    id = models.AutoField(
        db_column='PK_ITEM_FABRICANTE',
        primary_key=True
    )
    item = models.ForeignKey(
        Item,
        models.PROTECT,
        db_column='FK_ITEM',
        null=True,
        blank=True,
        verbose_name=Item._meta.verbose_name,
        related_name="item_fabricante"
    )
    fabricante = models.ForeignKey(
        Fabricante,
        models.PROTECT,
        db_column='FK_FABRICANTE',
        null=True,
        blank=True,
        verbose_name='Fabricante',
        related_name="item_fabricante"
    )
    tamanho_calcado = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="NU_TAMANHO"
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="NU_PRECO"
    )
    class Meta:
        verbose_name = 'Relação Item Fabricante'
        verbose_name_plural = 'Relações Itens Fabricantes'
        db_table = 'RL_ITEM_FABRICANTE'
        unique_together = ('item', 'fabricante')

    def __str__(self):
        return f'{self.item.nome} - {self.fabricante.nome} - {self.tamanho_calcado} - R${self.preco}'

    def save(self, *args, **kwargs):
        if self.item and self.item.nome:
            self.nome = self.item.nome[:35]
        super().save(*args, **kwargs)