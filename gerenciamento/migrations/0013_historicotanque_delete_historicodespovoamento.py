# Generated by Django 5.1.4 on 2025-02-12 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0012_remove_tanque_quantidade_atual_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoTanque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('P', 'Povoamento'), ('D', 'Despovoamento')], max_length=1)),
                ('quantidade', models.PositiveIntegerField()),
                ('data', models.DateField()),
                ('observacoes', models.TextField(blank=True)),
                ('taxa_sobrevivencia', models.FloatField(blank=True, null=True)),
                ('especie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gerenciamento.alevino')),
                ('tanque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico', to='gerenciamento.tanque')),
            ],
        ),
        migrations.DeleteModel(
            name='HistoricoDespovoamento',
        ),
    ]
