from django.db import transaction

from apps.lojas.models import Loja
from apps.vinculos.exception import VinculoExisteException, VinculoErroGenericoException
from apps.vinculos.models import Vinculo


class VinculoDomain:

    def __init__(self, vinculo: Vinculo):
        self.vinculo = vinculo

    @staticmethod
    def new_instance_by_id(vinculo_id: int) -> 'VinculoDomain':
        vinculo = Vinculo.objects.get(id=vinculo_id)
        return VinculoDomain(
            vinculo=vinculo
        )

    def get_vinculo(self):
        return Vinculo.objects.get(id=self.vinculo.id)

    def filtro_loja(self):
        if self.vinculo.PerfilVinculo.ADMIN:
            return Loja.objects.all().distinct()
        else:
            return Loja.objects.filter(vinculos__loja=self.vinculo.loja, vinculos__status=0).distinct()


    @staticmethod
    def vinculo_ativo(cpf):
        return Vinculo.objects.filter(usuario__cliente__cpf=cpf, status=0).exists()



    @transaction.atomic
    def salvar(self, user) -> Vinculo:
        try:
            self.vinculo.usuario = user
            self.vinculo.save()
            return self.vinculo
        except (VinculoExisteException,) as e:
            raise e
        except Exception:
            raise VinculoErroGenericoException

class VinculosFiltroDomain:
    def __init__(self, lojas, cpf=None, nome=None, loja_nome=None, perfil=None, status=None):
        self.lojas = lojas
        self.cpf = cpf
        self.nome = nome
        self.loja_nome = loja_nome
        self.perfil = perfil
        self.status = status

    def filtrar(self):
        vinculos = Vinculo.objects.select_related('usuario__cliente', 'loja').filter(loja__in=self.lojas)

        if self.cpf:
            vinculos = vinculos.filter(usuario__cliente__cpf__icontains=self.cpf)
        if self.nome:
            vinculos = vinculos.filter(usuario__cliente__nome_completo__icontains=self.nome)
        if self.loja_nome:
            vinculos = vinculos.filter(loja__nome__icontains=self.loja_nome)
        if self.perfil != '':
            vinculos = vinculos.filter(perfil=self.perfil)
        if self.status != '':
            vinculos = vinculos.filter(status=self.status)

        return vinculos
