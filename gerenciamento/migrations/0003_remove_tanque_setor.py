# Generated by Django 5.1.4 on 2024-12-05 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0002_alevino_tanque_especie_alevino'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanque',
            name='setor',
        ),
    ]
