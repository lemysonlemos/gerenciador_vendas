from django.db.models import Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from apps.enderecos.models import Municipio


class BuscarMunicipioView(View):
    def get(self, request, *args, **kwargs):
        uf_id = request.GET.get('uf', None)
        term = request.GET.get('term', '')

        municipios = Municipio.objects.none()
        if uf_id:
            municipios = Municipio.objects.filter(uf_id=uf_id, nome__icontains=term).order_by('nome')

        results = [
            {'id': municipio.id, 'text': municipio.nome}
            for municipio in municipios
        ]
        return JsonResponse({'results': results})