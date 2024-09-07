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
            ticket_quantity=0,
            half_ticket_quantity=0,
            tickets_sold=0,
            tickets_available=0,
            half_tickets_available=0,
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

    
    def test_create_ticket_no_availability(self):
       
        self.event.tickets_available = 0
        self.event.save()

     
        self.event.refresh_from_db()

        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

    
        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 400  


    
    def test_create_half_ticket(self):
        
        ticket_data = {
            "half_ticket": True,
            "cart_payment": str(self.payment.uuid),
        }

        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 201
        ticket = Ticket.objects.get(event=self.event)

        assert ticket is not None
        assert ticket.half_ticket is True
        assert ticket.event == self.event
        assert ticket.cart_payment == self.payment

        self.event.refresh_from_db()
        assert self.event.half_tickets_available == 49
        assert self.event.tickets_sold == 1


    def test_list_tickets(self):
        
        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }
        self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')
        self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        
        response = self.client.get(reverse('event-tickets-list', args=[self.event.uuid]))
        assert response.status_code == 200
        assert len(response.data) == 2  
    

    def test_delete_ticket(self):

        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }
        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')
        ticket_uuid = response.data['uuid']

        response = self.client.delete(reverse('event-tickets-detail', args=[self.event.uuid, ticket_uuid]))
        assert response.status_code == 204  

        
        with pytest.raises(Ticket.DoesNotExist):
            Ticket.objects.get(uuid=ticket_uuid)

    
    def test_verify_ticket(self):
        
        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

   
        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')
        ticket_uuid = response.data['uuid']
        ticket = Ticket.objects.get(uuid=ticket_uuid)

     
        verify_data = {"hash": ticket.hash}
        response = self.client.patch(reverse('verify_ticket', args=[self.event.uuid]), verify_data, format='json')

        assert response.status_code == 200

        ticket.refresh_from_db()
        assert ticket.verified is True
