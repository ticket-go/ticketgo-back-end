# Generated by Django 5.0.4 on 2024-08-30 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_remove_ticket_purchase_ticket_cart_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Ingresso', 'verbose_name_plural': 'Ingressos'},
        ),
    ]