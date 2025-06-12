from django.db.models import Value
from django.db.models.functions import Concat
from django.http import JsonResponse

from apps.enderecos.models import Municipio


def buscar_municipio(request):
    termo = request.GET.get("term") or request.GET.get("q")
    estado = request.GET.get("estado")
    uf = request.GET.get("uf")
    as_dict = request.GET.get('as_dict')

    municipios = Municipio.objects.all()
    if estado:
        municipios = municipios.filter(uf__sigla=estado)
    if uf:
        municipios = municipios.filter(uf_id=uf)
    if termo:
        municipios = municipios.filter(nome__unaccent__icontains=termo).order_by('nome')[:20]

    retorno = list(municipios.annotate(text=Concat('nome', Value('/'), 'uf__sigla')).values("id", "text"))

    if as_dict:
        return JsonResponse({'results': retorno, 'more': False}, safe=False)
    return JsonResponse(retorno, safe=False)