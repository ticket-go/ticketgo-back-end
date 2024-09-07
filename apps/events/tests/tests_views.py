import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.events.models import Event
from apps.address.models import Address
from apps.users.models import CustomUser
from datetime import date, time

@pytest.mark.django_db
class TestEventViews:
    def setup_method(self):
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpassword"
        )

       
        login_data = {
            "username": "testuser",
            "password": "testpassword"
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

    def create_event(self):
       
        event_data = {
            "name": "Festival de Música",
            "date": date.today(),
            "time": time(18, 0),
            "description": "Um grande festival de música.",
            "category": "music",
            "status": "scheduled",
            "ticket_value": 100.00,
            "half_ticket_value": 50.00,
            "ticket_quantity": 100,
            "half_ticket_quantity": 50,
            "address": str(self.address.uuid),  
            "user": self.user.user_id  
        }

      
        response = self.client.post(reverse('event-list'), event_data, format='json')

      
        assert response.status_code == 201

   
        return Event.objects.get(uuid=response.data['uuid'])

    def test_create_event(self):
        
        self.create_event()

    def test_delete_event(self):
      
        event = self.create_event()

    
        response = self.client.delete(reverse('event-detail', args=[event.uuid]))

       
        assert response.status_code == 204

      
        with pytest.raises(Event.DoesNotExist):
            Event.objects.get(uuid=event.uuid)


    def test_update_event(self):
       
        event = self.create_event()

      
        updated_event_data = {
            "name": "Festival de Rock",
            "date": date.today(),
            "time": time(20, 0),
            "description": "Um grande festival de rock.",
            "category": "music",
            "status": "scheduled",
            "ticket_value": 150.00,
            "half_ticket_value": 75.00,
            "ticket_quantity": 200,
            "half_ticket_quantity": 100,
            "address": str(self.address.uuid), 
            "user": self.user.user_id  
        }

       
        response = self.client.put(reverse('event-detail', args=[event.uuid]), updated_event_data, format='json')

   
        assert response.status_code == 200

        updated_event = Event.objects.get(uuid=event.uuid)
        assert updated_event.name == "Festival de Rock"
        assert updated_event.time == time(20, 0)
        assert updated_event.ticket_value == 150.00
        assert updated_event.ticket_quantity == 200
    

    def test_partial_update_event(self):
       
        event = self.create_event()

     
        partial_update_data = {
            "name": "Festival de Música Atualizado"
        }

    
        response = self.client.patch(reverse('event-detail', args=[event.uuid]), partial_update_data, format='json')

  
        assert response.status_code == 200

   
        assert response.data["name"] == "Festival de Música Atualizado"


    
    def test_list_events(self):
        
        self.create_event()
        self.create_event()

     
        response = self.client.get(reverse('event-list'))
    
        assert response.status_code == 200

        assert len(response.data) == 2


    def test_retrieve_event(self):
        
        event = self.create_event()

       
        response = self.client.get(reverse('event-detail', args=[event.uuid]))

        
        assert response.status_code == 200

        assert response.data["name"] == event.name

    
    def test_create_event_invalid_data(self):
    
        event_data = {
            "date": date.today(),
            "time": time(18, 0),
            "description": "Um grande festival de música.",
            "category": "music",
            "status": "scheduled",
            "ticket_value": 100.00,
            "half_ticket_value": 50.00,
            "ticket_quantity": 100,
            "half_ticket_quantity": 50,
            "address": self.address.id,
            "user": self.user.user_id
        }

        response = self.client.post(reverse('event-list'), event_data, format='json')

       
        assert response.status_code == 400

        assert "name" in response.data


    def test_delete_no_existent_event(self):

        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = self.client.delete(reverse('event-detail', args=[fake_uuid]))

        assert response.status_code == 404

    
    def test_event_tickets_availability(self):
        event = self.create_event()

        event.tickets_sold = 50
        event.tickets_available = event.ticket_quantity - event.tickets_sold 
        event.save()

        response = self.client.get(reverse('event-detail', args=[event.uuid]))

        assert response.status_code == 200
        assert response.data["tickets_available"] == event.ticket_quantity - event.tickets_sold


