# Generated by Django 5.1.3 on 2024-11-29 11:27

from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('fluxo', '0003_fluxoagua_hora_alter_fluxoagua_consumo_diario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fluxoagua',
            name='hora',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),

    ]
