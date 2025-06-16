import django_filters

from apps.compras.models import Compra


class CompraFilter(django_filters.FilterSet):
    loja = django_filters.CharFilter(
        field_name='loja__nome',
        lookup_expr='icontains',
        label='Loja'
    )
    cliente = django_filters.CharFilter(
        field_name='cliente__nome',
        lookup_expr='icontains',
        label='Cliente'
    )
    vendedor = django_filters.CharFilter(
        field_name='vendedor__nome',
        lookup_expr='icontains',
        label='Vendedor'
    )
    finalizada = django_filters.BooleanFilter(
        field_name='compra_finalizada',
        label='Finalizada'
    )

    class Meta:
        model = Compra
        fields = ['loja', 'cliente', 'vendedor', 'finalizada']