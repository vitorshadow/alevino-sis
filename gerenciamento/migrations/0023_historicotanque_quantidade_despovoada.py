# Generated by Django 5.1.4 on 2025-03-03 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0022_notificacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicotanque',
            name='quantidade_despovoada',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
