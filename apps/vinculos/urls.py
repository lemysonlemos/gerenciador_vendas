app_name = 'vinculos'

from django.urls import path


urlpatterns = [
    # URLs Públicas
    path('novo/', novo, name='novo'),
]