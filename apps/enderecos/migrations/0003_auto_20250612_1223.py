from django.db import migrations
import requests

def criar_ufs_e_municipios(apps, schema_editor):
    UF = apps.get_model('enderecos', 'UnidadeFederativa')
    M = apps.get_model('enderecos', 'Municipio')

    # Primeiro, buscar todas as UFs pela API oficial IBGE
    uf_url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    uf_response = requests.get(uf_url)
    uf_response.raise_for_status()
    ufs = uf_response.json()

    # Criar ou atualizar UFs no banco
    for uf in ufs:
        UF.objects.update_or_create(
            id=uf['id'],
            defaults={'nome': uf['nome'], 'sigla': uf['sigla']}
        )

    # Para cada UF, buscar seus municípios via API IBGE e salvar no banco
    for uf in ufs:
        municipios_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf['sigla']}/municipios"
        mun_response = requests.get(municipios_url)
        mun_response.raise_for_status()
        municipios = mun_response.json()

        for m in municipios:
            M.objects.update_or_create(
                id=m['id'],
                defaults={
                    'nome': m['nome'],
                    'uf_id': uf['id'],
                    'lat': None,
                    'lon': None,
                }
            )

class Migration(migrations.Migration):

    dependencies = [
        ('enderecos', '0002_remove_municipio_cnpj_remove_municipio_cod_ibge'),
    ]

    operations = [
        migrations.RunPython(criar_ufs_e_municipios),
    ]
