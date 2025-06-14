from apps.estoques.view import menus, listar_estoque, adicionar_estoque, editar_estoque

app_name = 'estoques'

from django.urls import path

urlpatterns = [
    path('menus/', menus, name='menus'),
    path('listar_estoque/', listar_estoque, name='listar_estoque'),
    path('adicionar_estoque/', adicionar_estoque, name='adicionar_estoque'),
    path('editar_estoque/<int:id_estoque>', editar_estoque, name='editar_estoque'),
]