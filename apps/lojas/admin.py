from django.contrib import admin

from apps.lojas.models import Loja, LojaContato


class LojaContatoInline(admin.TabularInline):
    model = LojaContato
    extra = 1
    autocomplete_fields = ['contato']


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'endereco', 'descricao_resumida')
    search_fields = ('nome',)
    list_filter = ('status',)
    inlines = [LojaContatoInline]
    autocomplete_fields = ['endereco']
    readonly_fields = ('justificativa',)

    def descricao_resumida(self, obj):
        return (obj.descricao[:75] + '...') if obj.descricao and len(obj.descricao) > 75 else obj.descricao
    descricao_resumida.short_description = 'Descrição'


@admin.register(LojaContato)
class LojaContatoAdmin(admin.ModelAdmin):
    list_display = ('loja', 'contato')
    autocomplete_fields = ['loja', 'contato']
