from django.forms.utils import ErrorDict


def _transforma_em_tupla(item):
    try:
        return eval(item)
    except Exception:
        return item


class ClienteBaseException(Exception):
    code: str
    message: str

    def __init__(self, message, code, propag=None):
        if isinstance(message, ErrorDict):
            msg_erro = "".join([f"{''.join(error_msgs)}" for field, error_msgs in message.items()])
            message = msg_erro

        self.propag = str(propag) if propag else None
        super().__init__(message, code)

    def __str__(self):
        return self._msg_excecao(super().__str__(), self.propag)

    def _msg_excecao(self, *args):
        separador = ' > '
        msg_parts = []

        for item in args:
            tupla_erro = _transforma_em_tupla(item)
            if item and isinstance(tupla_erro, tuple):
                msg_parts.append(f"({tupla_erro[1]}: {tupla_erro[0]})")
            elif item:
                msg_parts.append(str(item))

        return separador.join(msg_parts)