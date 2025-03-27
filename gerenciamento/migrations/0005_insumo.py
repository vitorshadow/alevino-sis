# Generated by Django 5.1.4 on 2024-12-11 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0004_alter_tanque_quantidade_retirada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto', models.CharField(max_length=100)),
                ('quantidade_produto', models.PositiveIntegerField()),
                ('estoque_minimo', models.PositiveIntegerField()),
                ('data_compra', models.DateField()),
            ],
        ),
    ]
