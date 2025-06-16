from django.contrib import admin

from apps.autenticacao.models import Permissao, Modulo, Grupo, GrupoPermissao, UsuarioContato, UsuarioEndereco, Usuario, \
    UsuarioBase


@admin.register(UsuarioBase)
class UsuarioBaseAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('username',)
    list_filter = ('is_active', 'is_superuser', 'is_staff')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'status', 'user')
    search_fields = ('cliente__nome_completo', 'cliente__cpf')
    list_filter = ('status',)
    raw_id_fields = ('cliente', 'user')


@admin.register(UsuarioEndereco)
class UsuarioEnderecoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'endereco')


@admin.register(UsuarioContato)
class UsuarioContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'contato')


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao')
    search_fields = ('nome',)


@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'modulo')
    search_fields = ('nome', 'modulo__nome')
    list_filter = ('modulo',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    filter_horizontal = ('permissoes',)


@admin.register(GrupoPermissao)
class GrupoPermissaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'grupo', 'permissao')
    search_fields = ('grupo__nome', 'permissao__nome')
