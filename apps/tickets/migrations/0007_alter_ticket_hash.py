# Generated by Django 5.0.4 on 2024-09-07 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_alter_ticket_cart_payment_alter_ticket_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='hash',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]