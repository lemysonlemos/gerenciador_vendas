app_name = 'cliente'

from django.urls import path

from .views import cadastro, painel, perfil

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('painel/', painel, name='painel'),
    path('perfil/', perfil, name='perfil'),

    #cliente gestão
    # path('gestao/cadastro', gestao_cadastro, name='gestao_cadastro'),
]