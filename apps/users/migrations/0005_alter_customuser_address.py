# Generated by Django 5.0.4 on 2024-08-07 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_add_updated_by_and_more'),
        ('users', '0004_historicalcustomuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to='address.address', verbose_name='Endereço'),
        ),
    ]
