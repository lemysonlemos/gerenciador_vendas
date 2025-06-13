from apps.base.exceptions import ClienteBaseException


class VinculoErroGenericoException(ClienteBaseException):

    def __init__(self, message=None, propag=None):
        self.code = 'VIN-001'
        if not message:
            message = "Houve um erro ao processar os dados do vínculo. Verifique os dados e tente novamente."
        super().__init__(message, self.code, propag)


class VinculoExisteException(ClienteBaseException):

    def __init__(self, message=None, propag=None):
        self.code = 'VIN-002'
        if not message:
            message = "O vínculo solicitado já está cadastrado para o usuário."
        super().__init__(message, self.code, propag)


class VinculoAtivoException(ClienteBaseException):

    def __init__(self, message=None, propag=None):
        self.code = 'VIN-003'
        if not message:
            message = "O vínculo solicitado já está ativo."
        super().__init__(message, self.code, propag)
