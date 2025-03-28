# Generated by Django 5.1.4 on 2025-02-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0019_historicotanque'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.TextField()),
                ('lida', models.BooleanField(default=False)),
                ('link', models.CharField(blank=True, max_length=200)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-data_criacao'],
            },
        ),
    ]
