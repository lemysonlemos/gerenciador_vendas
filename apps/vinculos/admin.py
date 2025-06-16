from django.contrib import admin

from apps.vinculos.models import Vinculo


@admin.register(Vinculo)
class VinculoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario_nome',
        'loja',
        'perfil_display',
        'status_display',
        'data_autorizacao',
        'data_inativacao',
    )
    search_fields = (
        'usuario__cliente__nome_completo',
        'usuario__cliente__cpf',
        'loja__nome',
    )
    list_filter = (
        'status',
        'perfil',
        'data_autorizacao',
        'data_inativacao',
    )
    autocomplete_fields = (
        'usuario',
        'loja',
        'autorizado_por_usuario',
        'inativado_por_usuario',
    )
    readonly_fields = ('data_autorizacao', 'data_inativacao')

    def usuario_nome(self, obj):
        return f"{obj.usuario.cliente.nome_completo} ({obj.usuario.cliente.cpf})" if obj.usuario else "-"
    usuario_nome.short_description = 'Usuário'

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'

    def perfil_display(self, obj):
        return obj.get_perfil_display()
    perfil_display.short_description = 'Perfil'
