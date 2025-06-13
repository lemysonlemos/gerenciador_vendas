from dataclasses import dataclass
from typing import Iterator, Optional

from django.http import HttpRequest

from apps.autenticacao.models import UsuarioBase
from apps.cliente.models import AnexoCliente
from apps.contatos.models import Contato
from apps.enderecos.models import Endereco


@dataclass
class DadosClienteDTO:
    enderecos: Iterator[Endereco]
    contatos: Iterator[Contato]
    user: Optional[UsuarioBase] = None
    request: Optional[HttpRequest] = None
    anexo_cliente: Optional[AnexoCliente] = None
    enderecos_delete: Iterator[Endereco] = None
    contatos_delete: Iterator[Contato] = None