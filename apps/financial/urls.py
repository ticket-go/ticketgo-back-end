from django.urls import path

from apps.financial.api.views import GeneratePaymentLinkAPIView

urlpatterns = [
    path(
        "generate_link",
        GeneratePaymentLinkAPIView.as_view(),
        name="generate_link",
    ),
]
