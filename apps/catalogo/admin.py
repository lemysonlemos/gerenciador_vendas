from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from apps.catalogo.models import ItemFabricante, Fabricante, Item

@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nome', 'nome_reduzido', 'ativo')
    search_fields = ('nome', 'nome_reduzido')
    list_filter = ('ativo',)
    ordering = ('nome',)


@admin.register(Fabricante)
class FabricanteAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nome', 'nome_reduzido', 'ativo')
    search_fields = ('nome', 'nome_reduzido')
    list_filter = ('ativo',)
    ordering = ('nome',)


@admin.register(ItemFabricante)
class ItemFabricanteAdmin(ImportExportModelAdmin):
    list_display = ('id', 'item', 'fabricante', 'tamanho_calcado', 'preco', 'imagem_preview')
    search_fields = ('item__nome', 'fabricante__nome')
    list_filter = ('fabricante', 'item')
    ordering = ('item__nome',)

    def imagem_preview(self, obj):
        if obj.imagem:
            return f"<img src='{obj.imagem.url}' width='50' height='50' style='object-fit:cover;' />"
        return "-"
    imagem_preview.allow_tags = True
    imagem_preview.short_description = "Imagem"
