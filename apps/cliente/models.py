from datetime import timedelta, datetime, date
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteModel
from localflavor.br.models import BRCPFField

from apps.base.models import BaseModelDeleteLogico, BaseModel
from apps.base.utils import digits
from apps.cliente.managers import ClienteManager


def validate_file_extension(value):
    import os

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('A foto de perfil deve estar nos formatos .jpg, .jpeg ou .png')


def imagem_perfil_path(instance, filename):
    return f'fotos_perfil/img_{instance.id}_{filename}'


class Cliente(BaseModelDeleteLogico):
    SEXO_CHOICES = (
        ('I', "Ignorado"),
        ('M', "Masculino"),
        ('F', "Feminino")
    )
    RACA_CHOICES = (
        ('01', 'Branca'),
        ('02', 'Preta'),
        ('03', 'Parda'),
        ('04', 'Amarela'),
        ('05', 'Indígena'),
        ('99', 'Sem informação'),
    )


    id = models.AutoField(
        primary_key=True,
        db_column='PK_CLIENTE'
    )
    cpf = BRCPFField(
        max_length=11,
        verbose_name='CPF',
        db_column='CO_CPF',
        null=True,
        blank=True,
        unique=True,
        db_index=True
    )
    nome_completo = models.CharField(
        max_length=255,
        db_column='NO_NOME_COMPLETO',
        db_index=True
    )
    nome_social = models.CharField(
        db_column='NO_NOME_SOCIAL',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Nome Social'
    )
    nome_mae = models.CharField(
        db_column='NO_NOME_MAE',
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Nome da Mãe'
    )
    data_nascimento = models.DateField(
        verbose_name='data de nascimento',
        db_column='DT_NASCIMENTO',
        null=True,
        db_index=True
    )
    contato = models.ForeignKey(
        'contatos.Contato',
        related_name="cliente_contatos",
        verbose_name='contato',
        null=True,
        blank=True,
        db_column='FK_CONTATO',
        on_delete=models.PROTECT
    )
    contatos = models.ManyToManyField(
        'contatos.Contato',
        through='ClienteContato',
        through_fields=("cliente", "contato"),
    )
    endereco = models.ForeignKey(
        'enderecos.Endereco',
        related_name="clientes",
        verbose_name='endereço',
        db_column='FK_ENDERECO',
        on_delete=models.PROTECT
    )
    enderecos = models.ManyToManyField(
        'enderecos.Endereco',
        through='ClienteEndereco',
        through_fields=("cliente", "endereco"),
    )
    profissao = models.TextField(
        'Profissão ou trabalho',
        db_column='NO_PROFISSAO'
    )
    user = models.OneToOneField(
        'autenticacao.UsuarioBase',
        verbose_name='usuário',
        db_column='FK_USUARIO_BASE',
        on_delete=models.PROTECT
    )
    # cadastrador = models.ForeignKey(
    #     "vinculos.Vinculo",
    #     related_name="cidadaos",
    #     db_column='FK_CADASTRADOR',
    #     null=True,
    #     on_delete=models.PROTECT
    # )
    passaporte = models.CharField(
        max_length=8,
        db_column='NO_PASSAPORTE',
        null=True,
        blank=True
    )
    foto = models.FileField(
        max_length=200,
        upload_to=imagem_perfil_path,
        null=True,
        blank=True,
        db_column='NO_FOTO',
        validators=[validate_file_extension]
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        db_column="CO_SEXO",
        null=True
    )
    raca = models.CharField(
        max_length=2,
        choices=RACA_CHOICES,
        db_column="CO_RACA",
        null=True,
        verbose_name="Raça/Cor"
    )
    pais_origem = models.ForeignKey(
        'enderecos.Pais',
        related_name="clientes",
        verbose_name='País de origem',
        db_column='FK_PAIS_ORIGEM',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    naturalidade = models.ForeignKey(
        'enderecos.Municipio',
        related_name="clientes",
        verbose_name='Naturalidade',
        db_column='FK_MUNICIPIO_NATURALIDADE',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    historico = HistoricalRecords(
        related_name='historico_cliente',
    )
    historico_usuario_api = None

    objects = ClienteManager()

    def __str__(self):
        return self.nome_social if self.nome_social else self.nome_completo

    class Meta:
        verbose_name = 'Cliente'
        db_table = 'TB_CLIENTE'
        constraints = [
            models.CheckConstraint(
                check=Q(cpf__isnull=False) | Q(passaporte__isnull=False),
                name='not_both_null'
            )
        ]

    @classmethod
    def buscar(self, cpf):
        cpf = digits(cpf)
        retorno = self.objects.none()
        if len(cpf) == 11:
            qs = self.objects.filter(cpf=cpf)
            if qs.exists():
                retorno = qs.first()

        return retorno


    def get_nome(self):
        return self.nome_social or self.nome_completo


    def get_identificacao(self):
        retorno = self.nome_social or self.nome_completo
        if self.cpf:
            retorno += f' (CPF: {self.cpf})'
        return retorno


    @property
    def _history_user(self):
        return self.historico_usuario_api

    @_history_user.setter
    def _history_user(self, value):
        self.historico_usuario_api = value

    def clean(self):
        if self.data_nascimento and self.data_nascimento > datetime.now().date():
            raise ValidationError({'data_nascimento': 'A Data de Nascimento não pode ser maior que a data atual'})

        if self.cpf and len(self.cpf) < 11:
            raise ValidationError({'cpf': 'CPF Inválido'})
        super().clean()

    def get_cpf_formatado(self):
        if self.cpf:
            if len(self.cpf) == 14:
                return self.cpf
            else:
                value = self.cpf
                return value[:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:11]
        return '-'




class ClienteEndereco(BaseModel):
    id = models.AutoField(
        primary_key=True,
        db_column='PK_CLIENTE_ENDERECO'
    )
    cliente = models.ForeignKey(
        'cliente.Cliente',
        models.PROTECT,
        db_column='FK_CLIENTE',
        related_name='clientes_endereco'
    )
    endereco = models.ForeignKey(
        'enderecos.Endereco',
        models.PROTECT,
        db_column='FK_ENDERECO',
        related_name='enderecos_cliente',
    )

    class Meta:
        verbose_name = 'Endereço do cliente'
        db_table = 'RL_CLIENTE_ENDERECO'
        constraints = [
            UniqueConstraint(
                name='uk_cliente_endereco',
                fields=['cliente', 'endereco']
            )
        ]

    def save(self, *args, **kwargs):
        qs_cliente_tipo_endereco = ClienteEndereco.objects.filter(
            cliente=self.cliente,
            endereco__tipo_endereco=self.endereco.tipo_endereco
        )
        # if qs_cidadao_tipo_endereco.exists():
        #     raise CidadaoTipoEnderecoException()

        super().save(*args, **kwargs)


def anexo_cliente_path(instance, filename):
    return f'anexos_cliente/{instance.cliente.id}_{filename}'


class AnexoCliente(BaseModel):
    id = models.AutoField(
        primary_key=True,
        db_column='PK_ANEXO_CLIENTE'
    )
    arquivo = models.FileField(
        max_length=255,
        upload_to=anexo_cliente_path,
        db_column='NO_ARQUIVO'
    )
    cliente = models.ForeignKey(
        'cliente.Cliente',
        models.PROTECT,
        db_column='FK_CLIENTE',
        verbose_name=Cliente._meta.verbose_name
    )

    def __str__(self):
        return self.arquivo.url

    class Meta:
        db_table = 'TB_ANEXO_CLIENTE'



class ClienteContato(BaseModel):
    id = models.AutoField(
        db_column='PK_CLIENTE_CONTATO',
        primary_key=True
    )
    contato = models.ForeignKey(
        'contatos.Contato',
        on_delete=models.CASCADE,
        db_column='FK_CONTATO',
        related_name='contatos_cliente',
    )
    cliente = models.ForeignKey(
        'cliente.Cliente',
        on_delete=models.CASCADE,
        db_column='FK_CLIENTE',
        related_name='cliente_contatos'
    )

    class Meta:
        verbose_name = 'Contato do cliente'
        db_table = 'RL_CLIENTE_CONTATO'

    def __str__(self):
        return f"{self.cliente.nome_completo} - {self.contato}"










