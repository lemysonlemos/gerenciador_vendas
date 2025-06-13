from django.urls import path
from . import views


app_name = 'catalogo'

urlpatterns = [
    path('listar_catalogo/', views.listar_catalogo, name='listar_catalogo'),
    path('listar_catalogo_gestao/', views.listar_catalogo_gestao, name='listar_catalogo_gestao'),

    path('adicionar_catalogo/', views.adicionar_catalogo, name='adicionar_catalogo'),

]

