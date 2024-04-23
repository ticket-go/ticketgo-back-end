# Generated by Django 5.0.4 on 2024-04-23 17:22

import apps.utils.cpf_cnpj.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='cnpj',
            field=apps.utils.cpf_cnpj.models.CNPJField(max_length=18, verbose_name='CNPJ'),
        ),
    ]
