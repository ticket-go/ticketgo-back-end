# Generated by Django 5.0.4 on 2024-05-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0003_alter_payment_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo do pagamento'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pendente'), ('RECEIVED', 'Recebido'), ('CONFIRMED', 'Confirmado')], default='PENDING', max_length=50, verbose_name='Status'),
        ),
    ]
