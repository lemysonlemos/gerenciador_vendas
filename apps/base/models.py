from django.db import models
from django.db.models import Func
from softdelete.models import SoftDeleteModel


class BaseModel(models.Model):
    criado_em = models.DateTimeField(
        db_column='DT_CRIADO_EM',
        auto_now_add=True,
        auto_now=False,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        db_column='DT_ATUALIZADO_EM',
        auto_now_add=False,
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        abstract = True


class BaseModelDeleteLogico(SoftDeleteModel, BaseModel):
    class Meta:
        abstract = True


class MigrationsView(models.Model):
    id = models.IntegerField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class AdminLogView(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField()
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class FuncIdadePorUnidade(Func):
    """
    Calcula a idade por unidade.

    Args:
        expression (F): Condição do SQL.
        unit (str): 'year', 'month', 'day'.
    """
    function = 'DATE_PART'
    template = '%(function)s(\'%(unit)s\', age(%(expressions)s))'

    def __init__(self, expression, unit, **extra):
        super().__init__(expression, unit=unit, **extra)

    def as_sql(self, compiler, connection, context=None):
        sql, params = super().as_sql(compiler, connection, context)
        # Debug: Imprimir SQL e parâmetros
        print(f"SQL: {sql}, Params: {params}")
        return sql, params
