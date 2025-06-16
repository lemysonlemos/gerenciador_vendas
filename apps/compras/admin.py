from django.contrib import admin
from django.core.exceptions import ValidationError

from apps.compras.models import Compra, Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status')
    list_filter = ('status',)
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'catalogo',
        'loja',
        'pagamento',
        'vendedor',
        'qtd_compra',
        'status_compra_online',
        'compra_finalizada',
        'cancelar_compra',
    )
    list_filter = (
        'status_compra_online',
        'compra_finalizada',
        'cancelar_compra',
        'pagamento',
        'loja',
    )
    search_fields = (
        'cliente__nome_completo',
        'loja__nome',
    )
    autocomplete_fields = (
        'cliente',
        'estoque',
        'catalogo',
        'loja',
        'pagamento',
        'vendedor',
    )
    readonly_fields = ('estoque_disponivel',)

    def estoque_disponivel(self, obj):
        if obj.estoque:
            return f"{obj.estoque.qtd_estoque}"
        return "N/A"
    estoque_disponivel.short_description = "Estoque Disponível"

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, f"Erro ao salvar: {e}", level='error')
