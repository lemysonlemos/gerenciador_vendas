from django.urls import path
from . import views


app_name = 'catalogo'

urlpatterns = [
    path('listar_catalogo/', views.listar_catalogo, name='listar_catalogo'),
    path('listar_catalogo_gestao/', views.listar_catalogo_gestao, name='listar_catalogo_gestao'),

    path('adicionar_catalogo/', views.adicionar_catalogo, name='adicionar_catalogo'),
    path('editar_catalogo/<int:id_item_fabricante>', views.editar_catalogo, name='editar_catalogo'),

    path('adicionar_item/', views.adicionar_item, name='adicionar_item'),
    path('editar_item/<int:id_item_fabricante>', views.editar_item, name='editar_item'),

    path('adicionar_fabricante/', views.adicionar_fabricante, name='adicionar_fabricante'),
    path('editar_fabricante/<int:id_item_fabricante>', views.editar_fabricante, name='editar_fabricante'),

]

