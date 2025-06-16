from django.contrib import admin

from apps.enderecos.models import UnidadeFederativa, TipoEndereco, Municipio, Endereco, Pais


@admin.register(UnidadeFederativa)
class UnidadeFederativaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sigla']
    search_fields = ['nome', 'sigla']
    ordering = ['sigla']


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'uf', 'lat', 'lon']
    search_fields = ['nome', 'uf__nome', 'uf__sigla']
    list_filter = ['uf']
    ordering = ['nome']


@admin.register(TipoEndereco)
class TipoEnderecoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'criado_em', 'atualizado_em']
    search_fields = ['nome']
    ordering = ['nome']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['id', 'rua', 'numero', 'bairro', 'cep', 'municipio', 'tipo_endereco', 'lat', 'lon', 'criado_em']
    search_fields = ['rua', 'bairro', 'cep', 'municipio__nome', 'municipio__uf__nome']
    list_filter = ['tipo_endereco', 'municipio__uf']
    ordering = ['municipio__nome', 'bairro']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'nome_esp', 'nome_eng', 'sigla', 'criado_em', 'atualizado_em']
    search_fields = ['nome', 'nome_esp', 'nome_eng', 'sigla']
    ordering = ['nome']
    readonly_fields = ['criado_em', 'atualizado_em']
