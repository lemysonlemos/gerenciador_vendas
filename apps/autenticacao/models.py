from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel


def validate_file_extension(value):
    import os

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('A foto de perfil deve estar nos formatos .jpg, .jpeg ou .png')


def imagem_perfil_path(instance, filename):
    return f'fotos_perfil_gestao/img_{instance.id}_{filename}'

class UsuarioManager(BaseUserManager):

    def create_user(self, username, password=None):
        usuario = UsuarioBase(username=username)
        usuario.set_password(password)
        usuario.save()

    def create_superuser(self, username, password=None):
        usuario = UsuarioBase(username=username, is_staff=True)
        usuario.set_password(password)
        usuario.save()

class UsuarioBase(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=35,
        db_column='CO_USUARIO',
        verbose_name='CPF',
        unique=True,
    )
    is_active = models.BooleanField(
        db_column='ST_ATIVO',
        default=True
    )
    is_superuser = models.BooleanField(
        db_column='ST_SUPER',
        default=False
    )
    is_staff = models.BooleanField(
        db_column='ST_ADMIN',
        default=False
    )

    USERNAME_FIELD = 'username'

    vinculo_login = None

    objects = UsuarioManager()
    #
    # @property
    # def get_vinculo_login(self):
    #     return self.vinculo_login
    #
    # def has_perm(self, perm, obj=None):
    #     from apps.vinculos.models.vinculos_models import Vinculo, PerfilAcesso
    #     """
    #     Veririca as permissões dos usuários
    #
    #     - Verifica se o usuário está ativo se é superusuário e tá logado em um vinculo. Se essas condições forem
    #     satisfeitas o usuário terá permissão a tudo.
    #
    #     - Verifica se vincuo tá ativo, perfil tá ativo, permissao existe. Se essas condições forem satisfeitas, libera
    #     a funcionalidade.
    #     """
    #     if self.is_active and self.is_superuser and self.get_vinculo_login:
    #         return True
    #     try:
    #         vinculo = Vinculo.objects.get(pk=self.get_vinculo_login, status__in=[1, 3])
    #         acesso = PerfilAcesso.objects.filter(
    #             tipos_gestao__in=[vinculo.cadeia_frio.tipo_gestao],
    #             nivel_atuacao=vinculo.cadeia_frio.nivel_atuacao,
    #             perfil=vinculo.perfil,
    #             grupo__permissoes__nome=perm
    #         )
    #         if acesso.exists():
    #             return True
    #     except Exception:
    #         return False
    #
    #     return False

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuário base'
        verbose_name_plural = 'Usuários base'
        db_table = 'TB_USUARIO_BASE'


class Usuario(BaseModel):
    id = models.AutoField(
        db_column="PK_USUARIO",
        primary_key=True
    )
    cliente = models.ForeignKey(
        'cliente.Cliente',
        on_delete=models.PROTECT,
        db_column='FK_CLIENTE',
        null=True,
    )
    status = models.BooleanField(
        default=False,
        db_column="NO_STATUS"
    )
    user = models.OneToOneField(
        'autenticacao.UsuarioBase',
        related_name="usuario",
        on_delete=models.PROTECT,
        db_column='FK_USER',
        null=True,
    )
    historico = HistoricalRecords(
        related_name='historico_usuario'
    )
    historico_usuario_api = None

    def __str__(self):
        return f'{self.cliente.cpf} - {self.cliente.nome}'

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'TB_USUARIO'

    @property
    def _history_user(self):
        return self.historico_usuario_api

    @_history_user.setter
    def _history_user(self, value):
        self.historico_usuario_api = value



class UsuarioEndereco(models.Model):
    id = models.AutoField(
        db_column='PK_USUARIO_ENDERECO',
        primary_key=True
    )
    endereco = models.ForeignKey(
        'enderecos.Endereco',
        on_delete=models.CASCADE,
        db_column='FK_ENDERECO'
    )
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='FK_USUARIO'
    )

    class Meta:
        db_table = 'TB_USUARIO_ENDERECO'

    def __str__(self):
        return f"{self.usuario.cliente.nome_completo} - {self.endereco}"


class UsuarioContato(models.Model):
    id = models.AutoField(
        db_column='PK_USUARIO_CONTATO',
        primary_key=True
    )
    contato = models.ForeignKey(
        'contatos.Contato',
        on_delete=models.CASCADE,
        db_column='FK_CONTATO'
    )
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='FK_USUARIO'
    )

    class Meta:
        db_table = 'TB_USUARIO_CONTATO'

    def __str__(self):
        return f"{self.usuario.cliente.nome_completo} - {self.contato}"


class Modulo(BaseModel):
    id = models.AutoField(
        db_column="PK_MODULO",
        primary_key=True
    )
    nome = models.CharField(
        max_length=255,
        db_column='NO_MODULO',
        unique=True,
    )
    descricao = models.TextField(
        db_column='DS_MODULO'
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        db_table = 'TB_MODULO'


class Permissao(BaseModel):
    id = models.AutoField(
        db_column="PK_PERMISSAO",
        primary_key=True
    )
    nome = models.CharField(
        max_length=255,
        db_column='NO_PERMISSAO',
        unique=True,
    )
    descricao = models.TextField(
        db_column='DS_PERMISSAO'
    )
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.PROTECT,
        db_column='FK_MODULO'
    )

    def __str__(self):
        return f"{self.modulo.nome} - {self.nome}"

    class Meta:
        verbose_name = 'Permissao'
        verbose_name_plural = 'Permissões'
        db_table = 'TB_PERMISSAO'


class Grupo(BaseModel):
    id = models.AutoField(
        db_column="PK_GRUPO",
        primary_key=True
    )
    nome = models.CharField(
        max_length=255,
        db_column='NO_GRUPO',
        unique=True,
    )
    permissoes = models.ManyToManyField(
        Permissao,
        related_name="grupo_set",
        through='GrupoPermissao',
        through_fields=("grupo", "permissao"),
    )

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        db_table = 'TB_GRUPO'

    def __str__(self):
        return self.nome


class GrupoPermissao(BaseModel):
    id = models.AutoField(
        db_column="PK_GRUPO_PERMISSAO",
        primary_key=True
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.PROTECT,
        db_column="FK_GRUPO",
    )
    permissao = models.ForeignKey(
        Permissao,
        on_delete=models.PROTECT,
        db_column="FK_PERMISSAO",
    )

    class Meta:
        verbose_name = 'Relação Entre Grupo e Permissão'
        verbose_name_plural = 'Relação entre Grupos e Permissões'
        db_table = 'TB_GRUPO_PERMISSAO'