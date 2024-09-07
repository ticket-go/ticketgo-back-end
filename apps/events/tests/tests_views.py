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
