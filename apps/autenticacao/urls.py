from django.urls import path

from apps.autenticacao.views import login, login_funcionario, esqueceu_senha

app_name = 'autenticacao'

urlpatterns = [
    path('login/', login, name='login'),
    path('login_funcionario/', login_funcionario, name='login_funcionario'),
    path('esqueceu-senha/', esqueceu_senha, name='esqueceu_senha'),

]