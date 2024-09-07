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



