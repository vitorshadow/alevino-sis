# Generated by Django 5.1.4 on 2025-03-06 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0027_historicotanque_grupo_insumo_grupo_notificacao_grupo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tanque',
            name='data_povoamento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
