# Generated by Django 5.1.4 on 2025-02-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0011_tanque_quantidade_atual_historicodespovoamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanque',
            name='quantidade_atual',
        ),
        migrations.AddField(
            model_name='historicodespovoamento',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
    ]
