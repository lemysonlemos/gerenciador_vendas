import re
from django.db import models

from apps.base.models import BaseModel


class TipoContato(BaseModel):
    id = models.AutoField(
        db_column='PK_TIPO_CONTATO',
        primary_key=True
    )
    nome = models.CharField(
        max_length=255,
        db_column='NO_TIPO',
        unique=True
    )
    expressao_validacao = models.CharField(
        max_length=300,
        db_column='EXPRESSAO_VALIDACAO',
        null=True,
        blank=True
    )

    formato = models.CharField(
        max_length=300,
        db_column='FORMATO_VALIDACAO',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Tipo de Contato'
        verbose_name_plural = 'Tipos de Contato'
        db_table = 'TB_TIPO_CONTATO'

    def __str__(self):
        return self.nome


class Contato(BaseModel):
    id = models.AutoField(
        db_column='PK_CONTATO',
        primary_key=True
    )
    contato = models.CharField(
        max_length=255,
        db_column='NO_CONTATO',
        unique=False
    )
    tipo_contato = models.ForeignKey(
        'TipoContato',
        on_delete=models.PROTECT,
        db_column='FK_TIPO_CONTATO'
    )

    class Meta:
        db_table = 'TB_CONTATO'

    def __str__(self):
        return f"{self.tipo_contato.nome} : {self.contato}"

    # def save(self, *args, **kwargs):
    #     if self.tipo_contato.expressao_validacao:
    #         regex = re.compile(self.tipo_contato.expressao_validacao)
    #         if not regex.match(self.contato):
    #             raise ContatoRegexException()
    #     super().save(*args, **kwargs)
