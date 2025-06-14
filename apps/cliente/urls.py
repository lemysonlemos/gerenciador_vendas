app_name = 'cliente'

from django.urls import path

from .views import cadastro, painel, perfil, listar_clientes_gestao, adicionar_cliente_gestao, editar_cadastro

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('painel/', painel, name='painel'),
    path('perfil/', perfil, name='perfil'),

    #cliente gestão
    path('listar_clientes_gestao/', listar_clientes_gestao, name='listar_clientes_gestao'),
    path('adicionar_cliente_gestao/', adicionar_cliente_gestao, name='adicionar_cliente_gestao'),
    path('editar_cadastro/<int:id_cliente>/', editar_cadastro, name='editar_cadastro'),
]