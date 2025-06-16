from django.contrib import admin

from apps.estoques.models import Estoque, TipoTransacaoEstoque, TransacaoEstoque


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'catalogo',
        'loja',
        'qtd_estoque',
        'descricao',
    )
    list_filter = ('loja', 'catalogo__fabricante')
    search_fields = ('catalogo__item__nome', 'catalogo__fabricante__nome')



@admin.register(TipoTransacaoEstoque)
class TipoTransacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
        'sigla',
        'tipo'
    )
    list_filter = ('tipo',)
    search_fields = ('nome', 'sigla')


@admin.register(TransacaoEstoque)
class TransacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estoque',
        'tipo',
        'quantidade',
        'realizada_em',
        'registrada_em',
        'usuario_cadastro',
        'cancelada_por'
    )
    list_filter = (
        'tipo__tipo',
        'realizada_em',
        'registrada_em'
    )

