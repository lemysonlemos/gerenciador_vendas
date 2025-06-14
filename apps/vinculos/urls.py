from apps.autenticacao.views import login_funcionario
from apps.vinculos.views import listar_vinculos, adicionar_vinculo, editar_vinculo

from django.urls import path

app_name = 'vinculos'


urlpatterns = [
    path('', listar_vinculos, name='listar_vinculos'),
    path('adicionar/', adicionar_vinculo, name='adicionar_vinculo'),
    path('editar/<int:vinculo_id>/', editar_vinculo, name='editar_vinculo'),
    # URLs Públicas
    path('login_funcionario/', login_funcionario, name='login_funcionario'),

]