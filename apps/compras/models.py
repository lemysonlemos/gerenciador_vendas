from django.utils import timezone
from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.base.models import BaseModel


class Pagamento(BaseModel):
    id = models.AutoField(
        db_column='PK_PAGAMENTO',
        primary_key=True
    )
    nome = models.CharField(
        db_column='NO_PAGAMENTO',
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Pagamento'
    )
    status = models.BooleanField(
        db_column='ST_STATUS',
        default=True,
        verbose_name='Ativo',
    )

    class Meta:
        verbose_name = 'Pagamento'
        db_table = 'TB_PAGAMENTO'

    def __str__(self):
        return f"{self.nome}"


class Compra(BaseModel):
    id = models.AutoField(
        db_column='PK_COMPRA',
        primary_key=True
    )
    cliente = models.ForeignKey(
        'cliente.Cliente',
        models.PROTECT,
        db_column='FK_CLIENTE',
        verbose_name='Cliente',
        null=True,
    )
    estoque = models.ForeignKey(
        'estoques.Estoque',
        models.PROTECT,
        db_column='FK_ESTOQUE',
        verbose_name='Estoque',
        null=True,
    )
    catalogo = models.ForeignKey(
        'catalogo.ItemFabricante',
        models.PROTECT,
        db_column='FK_ITEM_FABRICANTE',
        verbose_name='Item_Fabricante',
        null=True,
    )
    loja = models.ForeignKey(
        'lojas.Loja',
        models.PROTECT,
        db_column='FK_LOJA',
        verbose_name='Loja',
        null=True,
    )
    pagamento = models.ForeignKey(
        Pagamento,
        models.PROTECT,
        db_column='FK_PAGAMENTO',
        verbose_name='PAGAMENTO',
        null=True,
    )
    vendedor = models.ForeignKey(
        'vinculos.Vinculo',
        models.PROTECT,
        db_column='FK_VINCULO',
        verbose_name='Vendedor',
        null=True,
    )
    qtd_compra = models.PositiveBigIntegerField(
        db_column='QT_COMPRA',
        blank=False,
        verbose_name='Quantidade Compra',
    )
    status_compra_online = models.BooleanField(
        db_column='ST_COMPRA_ONLINE',
        default=True,
        verbose_name='Compra_Online',
    )
    compra_finalizada = models.BooleanField(
        db_column='ST_COMPRA_FINALIZADA',
        default=False,
        verbose_name='Compra_Finalizada',
    )
    cancelar_compra = models.BooleanField(
        db_column='ST_CANCELAR_COMPRA',
        default=False,
        verbose_name='Cancelar_Compra',
    )
    dt_finalizacao = models.DateTimeField(
        db_column='DT_FINALIZACAO',
        auto_now_add=False,
        auto_now=False,
        verbose_name='Finalizado em',
        null=True,
    )

    dt_cancelamento = models.DateTimeField(
        db_column='DT_CANCELAMENTO',
        auto_now_add=False,
        auto_now=False,
        verbose_name='Cancelado em',
        null=True,
    )


    class Meta:
        verbose_name = 'Compra'
        db_table = 'TB_COMPRA'

    def __str__(self):
        return f"{self.cliente} - {self.catalogo} - {self.loja} - {self.pagamento}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            if self.estoque and self.qtd_compra:
                qtd_disponivel = self.estoque.qtd_estoque - self.estoque.qtd_reservada
                if qtd_disponivel < self.qtd_compra:
                    raise ValidationError("Quantidade em estoque insuficiente.")

                with transaction.atomic():
                    self.estoque.qtd_reservada += self.qtd_compra
                    self.estoque.save()
                    super().save(*args, **kwargs)
                return

        super().save(*args, **kwargs)

    def cancelar(self):
        if self.cancelar_compra:
            raise ValidationError("Esta compra já foi cancelada.")

        if not self.estoque:
            raise ValidationError("Compra sem estoque vinculado.")

        with transaction.atomic():
            self.cancelar_compra = True
            self.dt_cancelamento = timezone.now()
            self.estoque.qtd_reservada -= self.qtd_compra
            self.estoque.save()
            self.save()


    def finalizar(self):
        if self.compra_finalizada:
            raise ValidationError("Esta compra já foi finalizada.")

        if not self.estoque:
            raise ValidationError("Compra sem estoque vinculado.")

        if self.estoque.qtd_estoque < self.qtd_compra:
            raise ValidationError("Estoque insuficiente para finalização.")

        with transaction.atomic():
            self.compra_finalizada = True
            self.dt_finalizacao = timezone.now()
            self.estoque.qtd_estoque -= self.qtd_compra
            self.estoque.qtd_reservada -= self.qtd_compra
            self.estoque.save()
            self.save()


