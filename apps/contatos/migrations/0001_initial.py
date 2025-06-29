# Generated by Django 4.2.23 on 2025-06-12 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoContato',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True, db_column='DT_CRIADO_EM', verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, db_column='DT_ATUALIZADO_EM', verbose_name='Atualizado em')),
                ('id', models.AutoField(db_column='PK_TIPO_CONTATO', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='NO_TIPO', max_length=255, unique=True)),
                ('expressao_validacao', models.CharField(blank=True, db_column='EXPRESSAO_VALIDACAO', max_length=300, null=True)),
                ('formato', models.CharField(blank=True, db_column='FORMATO_VALIDACAO', max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'Tipo de Contato',
                'verbose_name_plural': 'Tipos de Contato',
                'db_table': 'TB_TIPO_CONTATO',
            },
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('criado_em', models.DateTimeField(auto_now_add=True, db_column='DT_CRIADO_EM', verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, db_column='DT_ATUALIZADO_EM', verbose_name='Atualizado em')),
                ('id', models.AutoField(db_column='PK_CONTATO', primary_key=True, serialize=False)),
                ('contato', models.CharField(db_column='NO_CONTATO', max_length=255)),
                ('tipo_contato', models.ForeignKey(db_column='FK_TIPO_CONTATO', on_delete=django.db.models.deletion.PROTECT, to='contatos.tipocontato')),
            ],
            options={
                'db_table': 'TB_CONTATO',
            },
        ),
    ]
