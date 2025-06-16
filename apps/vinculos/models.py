from django.db import models
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel


class Vinculo(BaseModel):

    class StatusVinculo(models.IntegerChoices):
        ATIVO = 0
        INATIVO = 1

    ATIVO = "Vínculo Ativo"
    INATIVO = "Vínculo Inativo"

    STATUS_CHOICES = (
        (0, ATIVO),
        (1, INATIVO),
    )
    class PerfilVinculo(models.IntegerChoices):
        ADMIN = 0
        VENDEDOR = 1
        GERENTE = 2

    ADMIN = 'Administrador'
    VENDEDOR = 'Vendedor'
    GERENTE = 'Gerente'

    STATUS_PERFIL = (
        (0, ADMIN),
        (1, VENDEDOR),
        (2, GERENTE),
    )
    id = models.AutoField(
        db_column="PK_VINCULO",
        primary_key=True
    )
    usuario = models.ForeignKey(
        'autenticacao.Usuario',
        related_name="vinculos",
        on_delete=models.PROTECT,
        db_column='FK_USUARIO',
        null=True,
    )
    loja = models.ForeignKey(
        'lojas.Loja',
        related_name="vinculos",
        on_delete=models.PROTECT,
        db_column='FK_LOJA',
        null=True,
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        db_column='ST_VINCULO',
        default=0,
        db_index=True
    )
    perfil = models.IntegerField(
        choices=STATUS_PERFIL,
        db_column='ST_PERFIL',
        default=1,
        db_index=True,
        null=True,
    )
    autorizado_por_usuario = models.ForeignKey(
        'autenticacao.Usuario',
        related_name="vinculos_autorizados",
        null=True,
        on_delete=models.PROTECT,
        db_column='AUTORIZADOR_POR',
    )
    data_autorizacao = models.DateTimeField(
        null=True,
        db_column="DT_AUTORIZACAO"
    )
    inativado_por_usuario = models.ForeignKey(
        'autenticacao.Usuario',
        related_name="vinculos_inativados",
        null=True,
        on_delete=models.PROTECT,
        db_column='INATIVADO_POR'
    )
    data_inativacao = models.DateTimeField(
        null=True,
        db_column="DT_INATIVACAO"
    )
    historico = HistoricalRecords(
        related_name='historico_vinculo'
    )
    historico_usuario_api = None

    # objects = VinculoManager()

    class Meta:
        verbose_name = 'Vínculo'
        verbose_name_plural = 'Vínculos'
        db_table = 'TB_USUARIO_VINCULO'

    def __str__(self):
        return f"{self.usuario.cliente.nome_completo} | {self.usuario.cliente.cpf}"