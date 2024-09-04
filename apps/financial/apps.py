from django.apps import AppConfig


class FinancialConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.financial"

    def ready(self):
        from apps.financial import asaas

        asaas.start()
