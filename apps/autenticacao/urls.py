from django.urls import path
from apps.autenticacao.views import login, inicio, login_funcionario

app_name = 'autenticacao'

urlpatterns = [
    path('login/', login, name='login'),
    path('login_funcionario/', login_funcionario, name='login_funcionario'),

]