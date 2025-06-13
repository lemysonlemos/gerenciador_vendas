from apps.autenticacao.views import login_funcionario
from apps.vinculos.views import novo, informar_cpf

from django.urls import path

app_name = 'vinculos'


urlpatterns = [
    # URLs Públicas
    path('novo/<int:id_cliente>', novo, name='novo'),
    path('login_funcionario/', login_funcionario, name='login_funcionario'),
    path('informar_cpf/', informar_cpf, name='informar_cpf'),
]