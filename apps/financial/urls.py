from django.urls import path

from apps.financial.api.views import InvoicesAPIView

urlpatterns = [
    path(
        "generate_invoice",
        InvoicesAPIView.as_view(),
        name="generate_invoices",
    ),
]
