# Generated by Django 5.1.4 on 2025-02-27 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0021_delete_notificacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.TextField()),
                ('tipo', models.CharField(choices=[('warning', 'Aviso'), ('danger', 'Crítico')], max_length=20)),
                ('lida', models.BooleanField(default=False)),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
