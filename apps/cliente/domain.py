from django.db import transaction, IntegrityError
from typing import Iterator
from django.contrib.auth import update_session_auth_hash

from apps.base.exceptions import ClienteBaseException
from apps.cliente.dataclasses import DadosClienteDTO
from apps.cliente.exceptions import ClienteEnderecoNuloException, ClienteErroGenericoException
from apps.cliente.models import Cliente, ClienteEndereco, ClienteContato
from apps.enderecos.models import Endereco


class ClienteDomain:

    def __init__(self, cliente):
        self.cliente = cliente


    @staticmethod
    def insstance_by_cliente(id_cliente: int):
        """
        Retorna uma nova instancia do ClienteDomain
        """
        cliente = Cliente.objects.get(id=id_cliente)
        return ClienteDomain(cliente=cliente)

    @staticmethod
    def get_busca_cpf(cpf):
        return Cliente.objects.filter(cpf=cpf).first()


    def get_contatos_cliente(self):
        return self.cliente.contatos.all()


    def get_enderecos_cliente(self):
        return self.cliente.enderecos.all()

    def __cliente_nao_possui_endereco(
            self, enderecos: Iterator[Endereco] = None, enderecos_delete: Iterator[Endereco] = None
    ) -> bool:
        if not self.cliente.id:
            return not enderecos

        if enderecos_delete is not None:
            qtd_enderecos = self.cliente.enderecos.count()
            return qtd_enderecos == len(enderecos_delete)
        return False

    @staticmethod
    def redefinir_senha(dados_cliente: DadosClienteDTO):
        user = dados_cliente.user
        request = dados_cliente.request
        user.save()
        if request:
            update_session_auth_hash(request, user)

    @transaction.atomic()
    def editar(self, dados_cliente: DadosClienteDTO) -> Cliente:
        try:
            enderecos_delete = dados_cliente.enderecos_delete
            contatos_delete = dados_cliente.contatos_delete
            enderecos = dados_cliente.enderecos
            contatos = dados_cliente.contatos

            for endereco in enderecos:
                endereco.save()
                ClienteEndereco.objects.get_or_create(cliente_id=self.cliente.id, endereco=endereco)

            for contato in contatos:
                contato.save()
                ClienteContato.objects.get_or_create(cliente_id=self.cliente.id, contato=contato)

            if self.__cliente_nao_possui_endereco(enderecos_delete=enderecos_delete):
                raise ClienteEnderecoNuloException()

            for endereco in enderecos_delete:
                ClienteEndereco.objects.get(cliente_id=self.cliente.id, endereco=endereco).delete()

            for contato in contatos_delete:
                ClienteContato.objects.get(cliente_id=self.cliente.id, contato=contato).delete()

            self.cliente.endereco = ClienteEndereco.objects.filter(cliente_id=self.cliente.id).first().endereco
            self.cliente.contato = None

            if ClienteContato.objects.filter(cliente_id=self.cliente.id).first():
                self.cliente.contato = ClienteContato.objects.filter(cliente_id=self.cliente.id).first().contato

            self.cliente.save()

            if dados_cliente.user:
                self.redefinir_senha(dados_cliente)

            return self.cliente
        except ClienteBaseException as e:
            raise e
        except IntegrityError:
            msg = ("Houve um erro ao salvar os dados do cliente. Por favor, verifique se já existe outro cliente "
                   "cadastrado com os seguintes dados:")
            if self.cliente.cpf:
                msg += f"CPF: {self.cliente.cpf}\n"
            raise ClienteErroGenericoException(message=msg)
        except Exception:
            raise ClienteErroGenericoException()