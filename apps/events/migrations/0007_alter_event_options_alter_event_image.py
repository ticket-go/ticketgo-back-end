# Generated by Django 5.0.4 on 2024-08-30 19:56

import apps.events.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_half_ticket_quantity_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Evento', 'verbose_name_plural': 'Eventos'},
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to=apps.events.models.event_image_upload_to, verbose_name='Banner'),
        ),
    ]
