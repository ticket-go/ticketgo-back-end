from django.urls import path
from .views import ProcessPaymentAPIView

urlpatterns = [
    path('proccess-payment/', ProcessPaymentAPIView.as_view(),name='proccess-payment'), 
]