# Generated by Django 5.1.4 on 2025-03-03 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0024_historicotanque_povoado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicotanque',
            name='povoado',
        ),
    ]
