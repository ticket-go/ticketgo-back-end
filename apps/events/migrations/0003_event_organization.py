# Generated by Django 5.0.4 on 2024-04-18 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_add_updated_by_and_more'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_organization', to='organizations.organization', verbose_name='Organização'),
        ),
    ]
