# Generated by Django 5.1.3 on 2024-11-29 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo', '0011_alter_fluxoagua_litros'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ConsumoDiarioModel',
            new_name='ConsumoDiario',
        ),
        migrations.RenameField(
            model_name='fluxoagua',
            old_name='litros',
            new_name='consumo_diario',
        ),
    ]
