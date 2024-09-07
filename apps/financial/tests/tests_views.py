import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.financial.models import CartPayment
from apps.users.models import CustomUser
from apps.address.models import Address


@pytest.mark.django_db
class TestCartPaymentsViewSet:

    def setup_method(self):
        self.client = APIClient()

        self.address = Address.objects.create(
            street="Rua Principal",
            number=123,
            district="Centro",
            city="São Paulo",
            state="SP",
            country="Brasil",
            zip_code="01000-000"
        )

        self.user = CustomUser.objects.create_user(
            username="michael",
            email="michael@michael.com",
            password="michael",
            first_name="Michael",
            last_name="Cesar",
            cpf="12345678909",  
            address=self.address
        )
        self.client.force_authenticate(user=self.user)
        

        
    def test_create_cart_payment(self):
        payment_data = {
            "value": 100.00,
            "payment_type": "CARD",
            "user": str(self.user.user_id)
        }

        response = self.client.post(reverse('cartpayment-list'), payment_data, format='json')
        assert response.status_code == 201
        assert CartPayment.objects.count() == 1




    def test_retrieve_cart_payment_history(self):
        payment = CartPayment.objects.create(
            value=100.00,
            payment_type="CARD",
            user=self.user
        )

        response = self.client.get(reverse('cartpayment-history', args=[payment.uuid]))
        assert response.status_code == 200
        assert "history_id" in response.data[0]



    def test_generate_invoice(self):
    
        payment = CartPayment.objects.create(
            value=150.00,
            payment_type="CARD",
            user=self.user
        )

        invoice_data = {
            "cart_payment": str(payment.uuid),
        }

     
        response = self.client.post(reverse('generate_invoices'), invoice_data, format='json')

        if response.status_code != 200:
            print("Response data:", response.data)
        
        assert response.status_code == 200



    def test_list_cart_payments_filter(self):
     
        CartPayment.objects.create(value=100.00, payment_type="CARD", status="PENDING", user=self.user)
        CartPayment.objects.create(value=200.00, payment_type="CARD", status="RECEIVED", user=self.user)

      
        response = self.client.get(reverse('cartpayment-list'), {'status': 'RECEIVED', 'user': str(self.user.user_id)}, format='json')
        
     
        assert response.status_code == 200
        
        
        assert len(response.data) == 1
        assert response.data[0]['status'] == 'RECEIVED'
