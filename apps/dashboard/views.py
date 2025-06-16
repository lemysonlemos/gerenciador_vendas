import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import json

from apps.compras.models import Compra
from apps.vinculos.domain import VinculoDomain


def dashboardcompras(request):
    usuario_id = request.user.usuario.id
    vinculo_domain = VinculoDomain.new_instance_by_id(usuario_id)
    lojas = vinculo_domain.filtro_loja()

    compras = Compra.objects.select_related(
        'cliente', 'catalogo__item', 'catalogo__fabricante',
        'loja', 'pagamento', 'vendedor'
    ).filter(loja__in=lojas)

    # Filtros GET
    loja_id = request.GET.get('loja')
    status_finalizada = request.GET.get('finalizada')
    status_cancelada = request.GET.get('cancelada')

    if loja_id:
        compras = compras.filter(loja__id=loja_id)
    if status_finalizada in ['sim', 'nao']:
        compras = compras.filter(compra_finalizada=(status_finalizada == 'sim'))
    if status_cancelada in ['sim', 'nao']:
        compras = compras.filter(cancelar_compra=(status_cancelada == 'sim'))

    # Exportação XLSX
    if request.GET.get('exportar') == 'xlsx':
        return exportar_relatorio_xlsx(compras)

    # Dados para gráfico
    dados_grafico = {
        'finalizadas': compras.filter(compra_finalizada=True).count(),
        'canceladas': compras.filter(cancelar_compra=True).count(),
        'online': compras.filter(status_compra_online=True).count(),
    }

    context = {
        'compras': compras,
        'lojas': lojas,
        'dados_grafico': json.dumps(dados_grafico),
    }
    return render(request, 'dashboard/dashboard_compras.html', context)


def exportar_relatorio_xlsx(compras):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Relatório de Compras"

    headers = [
        "Cliente", "Item", "Fabricante", "Tamanho", "Loja",
        "Pagamento", "Vendedor", "Qtd", "Online", "Finalizada", "Cancelada"
    ]
    ws.append(headers)

    for compra in compras:
        ws.append([
            str(compra.cliente),
            str(compra.catalogo.item.nome),
            str(compra.catalogo.fabricante.nome),
            str(compra.catalogo.tamanho_calcado),
            str(compra.loja),
            str(compra.pagamento),
            str(compra.vendedor),
            compra.qtd_compra,
            "Sim" if compra.status_compra_online else "Não",
            "Sim" if compra.compra_finalizada else "Não",
            "Sim" if compra.cancelar_compra else "Não",
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=relatorio_compras.xlsx'
    wb.save(response)
    return response
