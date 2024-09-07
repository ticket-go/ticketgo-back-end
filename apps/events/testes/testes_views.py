import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.events.models import Event
from apps.address.models import Address
from apps.users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, time

@pytest.mark.django_db
class TestEventViews:

    def setup_method(self):
        self.client = APIClient()

        self.address = Address.objects.create(
            street="Rua 1",
            number=123,
            district="Centro",
            city="Cidade X",
            state="RN",  
            country="Brasil",
            zip_code="12345-678",
            complement="Apto 101"
        )

        self.user = CustomUser.objects.create_user(
            username="organizer",
            email="organizer@example.com",
            password="organizerpass"
        )

     
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_event(self):
       
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
            "user": str(self.user.user_id)  
        }

        
        response = self.client.post(reverse('event-list'), event_data, format='json')

   
        assert response.status_code == 201
        
        assert Event.objects.filter(name="Festival de Música").exists()

