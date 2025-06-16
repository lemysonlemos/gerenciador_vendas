from django.contrib import admin

from apps.contatos.models import TipoContato, Contato


@admin.register(TipoContato)
class TipoContatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'expressao_validacao', 'formato', 'criado_em', 'atualizado_em']
    search_fields = ['nome', 'expressao_validacao', 'formato']
    list_filter = ['criado_em', 'atualizado_em']
    ordering = ['nome']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'contato', 'tipo_contato', 'criado_em', 'atualizado_em']
    search_fields = ['contato', 'tipo_contato__nome']
    list_filter = ['tipo_contato', 'criado_em']
    ordering = ['tipo_contato', 'contato']
    readonly_fields = ['criado_em', 'atualizado_em']