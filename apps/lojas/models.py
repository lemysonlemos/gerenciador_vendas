from django.db import models
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel


class Loja(BaseModel):
    id = models.AutoField(
        db_column='PK_LOJA',
        primary_key=True
    )
    nome = models.CharField(
        db_column='NO_LOJA',
        max_length=120,
        unique=True,
        verbose_name='Nome'
    )
    descricao = models.TextField(
        db_column='DS_LOJA',
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    status = models.BooleanField(
        db_column='ST_ATIVO',
        default=True
    )
    endereco = models.ForeignKey(
        'enderecos.Endereco',
        models.PROTECT,
        db_column='FK_ENDERECO',
        blank=True,
        null=True,
        verbose_name='enderecos.Endereco._meta.verbose_name',
        related_name="lojas"
    )
    contatos = models.ManyToManyField(
        'contatos.Contato',
        through='lojas.LojaContato',
        related_name='contatos',
    )
    historico = HistoricalRecords(
        related_name='historico_unidade'
    )
    justificativa = models.TextField(
        db_column='DS_JUSTIFICATIVA',
        verbose_name='Justificativa',
        null=True,
        blank=True
    )
    # objects = LojaManager()

    class Meta:
        verbose_name = 'Loja'
        db_table = 'TB_LOJA'

    def __str__(self):
        return f'{self.nome}'


class LojaContato(models.Model):
    id = models.AutoField(
        db_column='PK_LOJA_CONTATO',
        primary_key=True
    )
    contato = models.ForeignKey(
        'contatos.Contato',
        on_delete=models.CASCADE,
        db_column='FK_CONTATO'
    )
    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        db_column='FK_LOJA'
    )

    class Meta:
        db_table = 'TB_LOJA_CONTATO'

    def __str__(self):
        return f"{self.loja.nome} - {self.contato}"