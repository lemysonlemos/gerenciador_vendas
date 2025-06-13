from django.urls import path
from . import views


app_name = 'catalogo'

urlpatterns = [
    path('listar_catalogo/', views.listar_catalogo, name='listar_catalogo'),
]

