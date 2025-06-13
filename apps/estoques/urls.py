from apps.estoques.view import menus

app_name = 'estoques'

from django.urls import path

urlpatterns = [
    path('menus/', menus, name='menus'),
]