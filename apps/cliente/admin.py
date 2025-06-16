from django.contrib import admin

from apps.cliente.models import AnexoCliente, ClienteContato, ClienteEndereco, Cliente


class ClienteEnderecoInline(admin.TabularInline):
    model = ClienteEndereco
    extra = 1
    autocomplete_fields = ['endereco']


class ClienteContatoInline(admin.TabularInline):
    model = ClienteContato
    extra = 1
    autocomplete_fields = ['contato']


class AnexoClienteInline(admin.TabularInline):
    model = AnexoCliente
    extra = 1
    fields = ('arquivo',)
    readonly_fields = ('arquivo',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'data_nascimento', 'sexo', 'raca')
    search_fields = ('nome_completo', 'cpf', 'nome_social')
    list_filter = ('sexo', 'raca')
    autocomplete_fields = ['contato', 'endereco', 'user']
    inlines = [ClienteEnderecoInline, ClienteContatoInline, AnexoClienteInline]
    readonly_fields = ('foto_preview',)

    def foto_preview(self, obj):
        if obj.foto:
            return f'<img src="{obj.foto.url}" width="100" height="100" style="object-fit: cover;" />'
        return "Sem foto"
    foto_preview.short_description = "Prévia da Foto"
    foto_preview.allow_tags = True  # necessário se estiver usando versões antigas do Django


@admin.register(ClienteEndereco)
class ClienteEnderecoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'endereco')
    search_fields = ('cliente__nome_completo',)


@admin.register(ClienteContato)
class ClienteContatoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'contato')
    search_fields = ('cliente__nome_completo',)


@admin.register(AnexoCliente)
class AnexoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'arquivo')
    search_fields = ('cliente__nome_completo',)