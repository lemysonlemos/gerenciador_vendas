from django.core.management.base import BaseCommand, CommandError

from apps.autenticacao.models import UsuarioBase
from apps.lojas.models import Loja
from apps.vinculos.models import Vinculo


class Command(BaseCommand):
    help = 'Ativa o perfil admin'

    def add_arguments(self, parser):
        parser.add_argument('cpfs', nargs='+', type=str)

    def handle(self, *args, **options):
        for cpf in options['cpfs']:
            try:
                usuario_base = UsuarioBase.objects.get(username=f'{cpf}_cliente')
            except UsuarioBase.DoesNotExist:
                raise CommandError('CPF "%s" não existe' % cpf)
            loja = Loja.objects.get(id=1)
            Vinculo.objects.get_or_create(
                usuario=usuario_base.usuario,
                loja=loja,
                status=0,
                perfil=0
            )

            self.stdout.write(self.style.SUCCESS('Perfil do CPF "%s" foram ativados com sucesso' % cpf))
