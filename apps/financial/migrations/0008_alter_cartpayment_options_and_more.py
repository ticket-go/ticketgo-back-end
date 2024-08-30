# Generated by Django 5.0.4 on 2024-08-30 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0007_delete_purchase'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartpayment',
            options={'verbose_name': 'Compra', 'verbose_name_plural': 'Compras'},
        ),
        migrations.AlterModelOptions(
            name='historicalcartpayment',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Compra', 'verbose_name_plural': 'historical Compras'},
        ),
    ]
