from django.core.management.base import BaseCommand, CommandError

from apps.autenticacao.models import UsuarioBase


class Command(BaseCommand):
    help = 'Ativa superusuario admin'

    def add_arguments(self, parser):
        parser.add_argument('cpfs', nargs='+', type=str)

    def handle(self, *args, **options):
        for cpf in options['cpfs']:
            try:
                usuario_base = UsuarioBase.objects.get(username=f'{cpf}_cliente')
                usuario_base.is_staff = True
                usuario_base.is_superuser = True
                usuario_base.save()
            except UsuarioBase.DoesNotExist:
                raise CommandError('CPF "%s" não existe' % cpf)

            self.stdout.write(self.style.SUCCESS('CPF "%s" teve o status elevado com sucesso' % cpf))
