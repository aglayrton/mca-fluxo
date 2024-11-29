# Generated by Django 5.1.3 on 2024-11-29 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo', '0002_remove_fluxoagua_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='fluxoagua',
            name='hora',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora'),
        ),
        migrations.AlterField(
            model_name='fluxoagua',
            name='consumo_diario',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Consumo Diário'),
        ),
        migrations.AlterField(
            model_name='fluxoagua',
            name='data',
            field=models.DateField(verbose_name='Data'),
        ),
    ]
