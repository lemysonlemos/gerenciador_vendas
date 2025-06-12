from django.db import models

from apps.base.models import BaseModel


class UnidadeFederativa(models.Model):
    id = models.AutoField(
        db_column='PK_UNIDADE_FEDERATIVA',
        primary_key=True
    )
    nome = models.CharField(
        db_column='NO_UF',
        max_length=19
    )
    sigla = models.CharField(
        db_column='SG_UF',
        max_length=2
    )

    class Meta:
        verbose_name = 'Unidade Federativa'
        verbose_name_plural = 'Unidades Federativas'
        db_table = 'TB_UNIDADE_FEDERATIVA'

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    id = models.AutoField(
        db_column='PK_MUNICIPIO',
        primary_key=True
    )
    nome = models.CharField(
        db_column='NO_MUNICIPIO',
        max_length=50
    )
    cnpj = models.CharField(
        db_column='NU_CNPJ',
        max_length=18,
        null=True,
        blank=True
    )
    cod_ibge = models.PositiveIntegerField(
        db_column='CO_IBGE',
        unique=True
    )
    lat = models.DecimalField(
        db_column='CG_LATITUDE',
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name='Latitude'
    )
    lon = models.DecimalField(
        db_column='CG_LONGITUDE',
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name='Longitude'
    )
    uf = models.ForeignKey(
        UnidadeFederativa,
        models.PROTECT,
        db_column='FK_UF',
        verbose_name=UnidadeFederativa._meta.verbose_name
    )

    class Meta:
        verbose_name = 'Município'
        db_table = 'TB_MUNICIPIO'

    def __str__(self):
        return self.nome


class TipoEndereco(BaseModel):
    id = models.AutoField(
        db_column='PK_TIPO_ENDERECO',
        primary_key=True
    )
    nome = models.CharField(
        db_column='NO_TIPO_ENDERECO',
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipos de Endereço'
        db_table = 'TB_TIPO_ENDERECO'


class Endereco(BaseModel):
    id = models.AutoField(
        db_column='PK_ENDERECO',
        primary_key=True
    )
    rua = models.CharField(
        db_column='NO_RUA',
        max_length=250,
        blank=True,
        null=True
    )
    numero = models.CharField(
        db_column='NU_NUMERO',
        max_length=8,
        blank=True,
        null=True
    )
    complemento = models.CharField(
        db_column='NO_COMPLEMENTO',
        max_length=120,
        blank=True,
        null=True
    )
    bairro = models.CharField(
        db_column='NO_BAIRRO',
        max_length=120,
        null=True,
        blank=True
    )
    cep = models.CharField(
        db_column='CO_CEP',
        max_length=8,
        verbose_name='CEP',
        null=True,
        blank=True
    )
    municipio = models.ForeignKey(
        Municipio,
        models.PROTECT,
        db_column='FK_MUNICIPIO',
        verbose_name=Municipio._meta.verbose_name,
        related_name='enderecos',
    )
    tipo_endereco = models.ForeignKey(
        TipoEndereco,
        models.PROTECT,
        db_column='FK_TIPO_ENDERECO',
        verbose_name=TipoEndereco._meta.verbose_name,
        related_name='enderecos',
        default=1
    )
    lat = models.DecimalField(
        db_column='CG_LATITUDE',
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name='Latitude'
    )
    lon = models.DecimalField(
        db_column='CG_LONGITUDE',
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name='Longitude'
    )

    class Meta:
        verbose_name = 'Endereço'
        db_table = 'TB_ENDERECO'

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro} - {self.cep}, ' \
               f'{self.municipio.nome}/{self.municipio.uf.sigla}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Pais(BaseModel):
    id = models.AutoField(
        db_column='PK_PAIS',
        primary_key=True
    )
    nome = models.CharField(
        max_length=255,
        db_column='NO_PAIS'
    )
    nome_esp = models.CharField(
        max_length=255,
        db_column='NO_PAIS_ESP'
    )
    nome_eng = models.CharField(
        max_length=255,
        db_column='NO_PAIS_ENG'
    )
    sigla = models.CharField(
        max_length=2,
        db_column='CO_SIGLA'
    )

    class Meta:
        verbose_name = 'País'
        db_table = 'TB_PAIS'

    def __str__(self):
        return self.nome
