from apps.lojas.views import listar_lojas, editar_loja, adicionar_loja

app_name = 'lojas'

from django.urls import path

urlpatterns = [
    path('', listar_lojas, name='listar_lojas'),
    path('editar/<int:id_loja>/', editar_loja, name='editar_loja'),
    path('adicionar/', adicionar_loja, name='adicionar_loja'),
]