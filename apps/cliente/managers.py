from softdelete.managers import SoftDeleteManager


class ClienteManager(SoftDeleteManager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'endereco',
            'contato',
            'user',
        )
