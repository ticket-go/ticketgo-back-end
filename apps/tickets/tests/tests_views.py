import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.tickets.models import Ticket
from apps.events.models import Event
from apps.address.models import Address
from apps.financial.models import CartPayment
from apps.users.models import CustomUser
from datetime import date, time

@pytest.mark.django_db
class TestTicketViews:

    def setup_method(self):
        self.client = APIClient()

      
        self.user = CustomUser.objects.create_user(
            username="michael",
            email="michael@michael.com",
            password="michael"
        )

        login_data = {
            "username": "michael",
            "password": "michael"
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        token = response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    
        self.address = Address.objects.create(
            street="Rua 1",
            number=123,
            district="Centro",
            city="Mossoró",
            state="RN",
            country="Brasil",
            zip_code="59600-000"
        )

      
        self.event = Event.objects.create(
            name="Festival de Música",
            date=date.today(),
            time=time(18, 0),
            description="Um grande festival de música.",
            category="music",
            status="scheduled",
            ticket_value=100.00,
            half_ticket_value=50.00,
            ticket_quantity=100,
            half_ticket_quantity=50,
            tickets_sold=0,
            tickets_available=100,
            half_tickets_available=50,
            address=self.address,  
            user=self.user,
        )

       
        self.payment = CartPayment.objects.create(
            value=0,
            status="PENDING",
            payment_type="CARD"
        )

    def test_create_ticket_full(self):
       
        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 201
        ticket = Ticket.objects.get(event=self.event)

        assert ticket is not None
        assert ticket.event == self.event
        assert ticket.cart_payment == self.payment
        assert ticket.half_ticket == False

        self.event.refresh_from_db()
        assert self.event.tickets_available == 99
        assert self.event.tickets_sold == 1

