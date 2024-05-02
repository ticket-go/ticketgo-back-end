from django.urls import path
from .views import PaymentAPIView

urlpatterns = [
    path('proccess-payment/', PaymentAPIView.as_view(),name='proccess-payment'), 
]