# Generated by Django 5.1.4 on 2025-02-04 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0007_tanque_estado_alter_tanque_data_retirada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanque',
            name='estado',
        ),
    ]
