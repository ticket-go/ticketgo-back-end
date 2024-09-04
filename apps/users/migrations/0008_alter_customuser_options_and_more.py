# Generated by Django 5.0.4 on 2024-08-30 19:54

import apps.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_cnpj_historicalcustomuser_cnpj'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Usuário', 'verbose_name_plural': 'Usuários'},
        ),
        migrations.AlterModelOptions(
            name='historicalcustomuser',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Usuário', 'verbose_name_plural': 'historical Usuários'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, upload_to=apps.users.models.user_image_upload_to, verbose_name='Imagem do Usuário'),
        ),
        migrations.AddField(
            model_name='historicalcustomuser',
            name='image',
            field=models.TextField(blank=True, max_length=100, verbose_name='Imagem do Usuário'),
        ),
    ]