from django.urls import path

from apps.dashboard.views import dashboardcompras

app_name = 'dashboard'

urlpatterns = [
    path('dashboardcompras/', dashboardcompras, name='dashboard_compras'),

]