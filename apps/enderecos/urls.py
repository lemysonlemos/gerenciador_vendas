
from django.urls import path

from apps.enderecos.data_views import BuscarMunicipioView

app_name = 'enderecos'

urlpatterns = [
    path('enderecos/data-view/buscar-municipio/', BuscarMunicipioView.as_view(), name='buscar_municipio'),
]