from django.urls import path

from apps.compras.views import listar_compras, listar_compras_cliente, compra_cliente, compra_cancelada, compra_vendedor

app_name = 'compras'

urlpatterns = [
    path('', listar_compras, name='listar_compras'),
    path('listar_compras_cliente', listar_compras_cliente, name='listar_compras_cliente'),
    path('compra_cliente/', compra_cliente, name='compra_cliente'),
    path('compra_vendedor/<int:id_estoque>', compra_vendedor, name='compra_vendedor'),
    path('compra_cancelada/<int:id_compra>', compra_cancelada, name='compra_cancelada'),
]