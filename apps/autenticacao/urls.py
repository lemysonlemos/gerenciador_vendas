from django.urls import path
from apps.autenticacao.views import login, inicio

app_name = 'autenticacao'

urlpatterns = [
    path('login/', login, name='login'),

]