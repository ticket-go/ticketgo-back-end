# Generated by Django 5.0.4 on 2024-09-06 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
    ]
