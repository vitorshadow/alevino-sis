# Generated by Django 5.1.4 on 2025-02-18 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0013_historicotanque_delete_historicodespovoamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetiradaParcial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('data', models.DateField()),
                ('finalizada', models.BooleanField(default=False)),
                ('tanque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retiradas_parciais', to='gerenciamento.tanque')),
            ],
        ),
        migrations.DeleteModel(
            name='HistoricoTanque',
        ),
    ]
