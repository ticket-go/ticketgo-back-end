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
            email="michael.cesar@escolar.ifrn.edu.br",
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
            half_ticket_quantity=100,
            tickets_sold=0,
            tickets_available=100,
            half_tickets_available=25,
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
        
        
        self.event.tickets_sold = 100
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
        assert self.event.half_tickets_available == 24
        assert self.event.tickets_sold == 1


    def test_create_halfticket_no_availability(self):

        #Observação: A disponibilidade do ingresso do tipo "meia" é baseado no número de ingressos disponíveis e não nos vendidos.
        self.event.half_tickets_available = 0
        self.event.save() 

    
        self.event.refresh_from_db()

      
        ticket_data = {
            "half_ticket": True, 
            "cart_payment": str(self.payment.uuid),
        }

     
        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 400



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


    def test_email(self, monkeypatch):
       
        def mock_send_email_with_attachment(ticket, attachment):
            pass 

        monkeypatch.setattr('apps.tickets.views.TicketEmailService.send_email_with_attachment', mock_send_email_with_attachment)

        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 201
    

    def test_pending_payment(self):
        
        self.payment.status = "PENDING"
        self.payment.save()

        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 201
        ticket = Ticket.objects.get(event=self.event)
        assert ticket.cart_payment.status == "PENDING"


    def test_create_ticket_after_event(self):
        
        self.event.date = date(2020, 1, 1)
        self.event.save()

        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 400
        assert response.data['error'] == 'Não é possível comprar ingressos para eventos que já ocorreram.'
    

    def test_confirmed_tickets(self):
       
        pending_payment = CartPayment.objects.create(value=100, status="PENDING", payment_type="CARD")
        confirmed_payment = CartPayment.objects.create(value=100, status="RECEIVED", payment_type="CARD")

        Ticket.objects.create(event=self.event, user=self.user, cart_payment=pending_payment, half_ticket=False)
        Ticket.objects.create(event=self.event, user=self.user, cart_payment=confirmed_payment, half_ticket=False)

        response = self.client.get(reverse('event-tickets-confirmed', args=[self.event.uuid]))

        assert response.status_code == 200
        assert len(response.data) == 1  
    

    def test_ticket_already_used(self):
    
        ticket = Ticket.objects.create(event=self.event, user=self.user, cart_payment=self.payment, half_ticket=False, verified=True)

        verify_data = {"hash": ticket.hash}
        response = self.client.patch(reverse('verify_ticket', args=[self.event.uuid]), verify_data, format='json')

        assert response.status_code == 409
        assert response.data['message'] == "Este ingresso já foi verificado. Por favor, verifique outro ingresso ou entre em contato com o suporte se você achar que isso é um erro."
    

    def test_cancel_ticket_updates_event(self):
      
        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }
        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')
        ticket_uuid = response.data['uuid']

    
        response = self.client.delete(reverse('event-tickets-detail', args=[self.event.uuid, ticket_uuid]))
        assert response.status_code == 204

       
        self.event.refresh_from_db()
        assert self.event.tickets_available == 100  
    

    def test_create_ticket_invalid_data(self):
       
        ticket_data = {
            "half_ticket": False,
            "cart_payment": ""
        }

        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 400  


    def test_create_ticket_for_future(self):
       
        self.event.date = date.today().replace(year=2025)
        self.event.save()

        ticket_data = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

        response = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data, format='json')

        assert response.status_code == 201 


    def test_ticket_qr_code(self):
     
        ticket_data_1 = {
            "half_ticket": False,
            "cart_payment": str(self.payment.uuid),
        }

        response_1 = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data_1, format='json')
        assert response_1.status_code == 201

    
        self.payment_2 = CartPayment.objects.create(
            value=0,
            status="PENDING",
            payment_type="CARD"
        )

        ticket_data_2 = {
            "half_ticket": True,
            "cart_payment": str(self.payment_2.uuid),
        }

        response_2 = self.client.post(reverse('event-tickets-list', args=[self.event.uuid]), ticket_data_2, format='json')
        assert response_2.status_code == 201

        ticket_1 = Ticket.objects.get(cart_payment=self.payment)
        ticket_2 = Ticket.objects.get(cart_payment=self.payment_2)

    
        assert ticket_1.hash is not None
        assert len(ticket_1.hash) > 0
        assert ticket_2.hash is not None
        assert len(ticket_2.hash) > 0

        assert ticket_1.hash != ticket_2.hash



    def test_invalid_hash(self):

        verify_data = {"hash": "invalidhash"}
        response = self.client.patch(reverse('verify_ticket', args=[self.event.uuid]), verify_data, format='json')
        assert response.status_code == 404
