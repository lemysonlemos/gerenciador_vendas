from django.urls import path

from apps.base.views import acesso_negado

app_name = 'base'

urlpatterns = [
    path('acesso-negado/', acesso_negado, name='acesso_negado'),
]