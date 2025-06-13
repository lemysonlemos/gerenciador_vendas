from apps.base.exceptions import ClienteBaseException


class ClienteErroGenericoException(ClienteBaseException):
    def __init__(self, message=None, propag=None):
        self.code = 'CLI-001'
        if not message:
            message = "Houve um erro ao processar os dados do cliente. Verifique os dados e tente novamente."
        super().__init__(message, self.code, propag)


class ClienteEnderecoNuloException(ClienteBaseException):

    def __init__(self, message=None, propag=None):
        self.code = 'CLI-002'
        if not message:
            message = "O cliente precisa ter ao menos um endereço."
        super().__init__(message, self.code, propag)