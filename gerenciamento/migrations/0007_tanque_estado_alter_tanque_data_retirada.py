# Generated by Django 5.1.4 on 2025-02-04 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0006_tanque_observacoes_tanque_previsao_retirada_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanque',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tanque',
            name='data_retirada',
            field=models.DateField(blank=True, null=True),
        ),
    ]
