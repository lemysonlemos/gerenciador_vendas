# Generated by Django 4.2.23 on 2025-06-14 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoques', '0002_estoque_loja_historicalestoque_loja_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estoque',
            name='perda_tecnica',
        ),
        migrations.RemoveField(
            model_name='estoque',
            name='qtd_bloqueada',
        ),
        migrations.RemoveField(
            model_name='estoque',
            name='qtd_reservada',
        ),
        migrations.RemoveField(
            model_name='historicalestoque',
            name='perda_tecnica',
        ),
        migrations.RemoveField(
            model_name='historicalestoque',
            name='qtd_bloqueada',
        ),
        migrations.RemoveField(
            model_name='historicalestoque',
            name='qtd_reservada',
        ),
    ]
