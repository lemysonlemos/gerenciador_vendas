"""gerenciador URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.autenticacao.views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
    path('select2/', include('django_select2.urls')),
    path('admin/', admin.site.urls),
    path('cliente/', include('apps.cliente.urls', namespace='cliente')),
    path('base/', include('apps.base.urls', namespace='base')),
    path('contatos/', include('apps.contatos.urls', namespace='contatos')),
    path('enderecos/', include('apps.enderecos.urls', namespace='enderecos')),
    path('autenticacao/', include('apps.autenticacao.urls', namespace='autenticacao')),
    path('estoques/', include('apps.estoques.urls', namespace='estoques')),
    path('catalogo/', include('apps.catalogo.urls', namespace='catalogo')),

    path('vinculos/', include('apps.vinculos.urls', namespace='vinculos')),

    path('lojas/', include('apps.lojas.urls', namespace='lojas')),
]
