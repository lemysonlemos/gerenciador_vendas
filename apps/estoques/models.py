from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType

from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel


class Estoque(BaseModel):
    id = models.AutoField(
        db_column='PK_ESTOQUE',
        primary_key=True
    )
    qtd_estoque = models.PositiveBigIntegerField(
        db_column='QT_ESTOQUE',
        blank=False,
        verbose_name='Quantidade liberada do itens',
        default=0,
    )
    catalogo = models.ForeignKey(
        'catalogo.ItemFabricante',
        models.PROTECT,
        db_column='FK_ITEM_FABRICANTE',
        verbose_name='Item_Fabricante',
        default=1
    )
    loja = models.ForeignKey(
        'lojas.Loja',
        models.PROTECT,
        db_column='FK_LOJA',
        verbose_name='Loja',
        null=True,
    )
    historico = HistoricalRecords(
        related_name='historico_estoque'
    )
    descricao = models.CharField(
        max_length=500,
        db_column='NO_DESCRICAO',
        null=True,
        blank=True,
        verbose_name='Descrição'
    )
    class Meta:
        verbose_name = 'Estoque'
        db_table = 'TB_ESTOQUE'

    def __str__(self):
        return f"{self.catalogo.item.nome} - {self.catalogo.fabricante.nome} - {self.catalogo.tamanho_calcado} - {self.catalogo.preco}"



class TipoTransacaoEstoque(models.Model):
    class TipoTransacaoEstoqueID(models.IntegerChoices):
        COMPRA = 1
        CANCELAMENTO_COMPRA = 2
        VENDA = 3
        CANCELAMENTO_VENDA = 4
        PERCA_TECNICA = 5
        DEVOLUCAO = 6

    class TipoTransacao(models.TextChoices):
        ENTRADA = 'E', 'Entrada'
        SAIDA = 'S', 'Saída'


    id = models.IntegerField(
        primary_key=True,
        db_column='PK_TIPO_TRANSACAO',
        choices=TipoTransacaoEstoqueID.choices,
    )
    nome = models.CharField(
        max_length=100,
        db_column='NOME',
        unique=True
    )
    sigla = models.CharField(
        max_length=5,
        db_column='SIGLA',
        unique=True
    )
    tipo = models.CharField(
        max_length=1,
        choices=TipoTransacao.choices,
        db_column='TIPO',
    )

    class Meta:
        db_table = 'TB_TIPO_TRANSACAO_ESTOQUE'

    def __str__(self):
        return self.nome


class TransacaoEstoque(models.Model):
    estoque = models.ForeignKey(
        Estoque,
        models.PROTECT,
        db_column='FK_ESTOQUE',
    )
    tipo = models.ForeignKey(
        TipoTransacaoEstoque,
        models.PROTECT,
        db_column='PK_TIPO_TRANSACAO',
    )
    chave_transacao = models.IntegerField(
        db_column='CHAVE_TRANSACAO'
    )
    quantidade = models.IntegerField(
        db_column='QUANTIDADE',
    )
    realizada_em = models.DateTimeField(
        db_column='DT_REALIZADA_EM'
    )
    registrada_em = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        db_column='DT_CADASTRADO_EM',
    )
    usuario_cadastro = models.ForeignKey(
        'vinculos.Vinculo',
        models.PROTECT,
        db_column='FK_USUARIO_CADASTRO',
        verbose_name='Usuário que cadastrou a transação do estoque',
        null=True,
    )
    cancelada_por = models.ForeignKey(
        'self',
        models.PROTECT,
        db_column='FK_TRANSACAO_REVERSAO',
        null=True,
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        models.PROTECT
    )
    content_object = GenericForeignKey(
        'content_type',
        'chave_transacao'
    )
    observacao = models.CharField(
        max_length=255,
        db_column='DS_OBSERVACAO',
        null=True,
        blank=True,
        verbose_name='Observação'
    )

    class Meta:
        db_table = 'TB_TRANSACAO_ESTOQUE'
        verbose_name = 'Transação do estoque'
        verbose_name_plural = 'Transações dos estoques'