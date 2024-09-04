import os
from django.apps import AppConfig


class FinancialConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.financial"

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            from apps.financial import asaas
            print('APscheduler running...')
            asaas.start()
