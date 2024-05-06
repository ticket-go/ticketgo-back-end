from django.urls import path
from .views import PaymentAPIView, test


urlpatterns = [
    path('process-payment', PaymentAPIView.as_view()),
    path('test/', test),
]