# Generated by Django 5.1.4 on 2025-03-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0023_historicotanque_quantidade_despovoada'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicotanque',
            name='povoado',
            field=models.BooleanField(default=True),
        ),
    ]
