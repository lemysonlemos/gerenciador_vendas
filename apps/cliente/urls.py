app_name = 'cliente'

from django.urls import path

from .views import cadastro, painel

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('painel/', painel, name='painel'),
]