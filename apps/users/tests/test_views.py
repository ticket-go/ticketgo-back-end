import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import CustomUser

@pytest.mark.django_db
class TestUserViews:
    username = "michael"
    email = "michael@michael.com"
    password = "michael"
    cpf = "12345678909"

    def setup_method(self):
        
        self.client = APIClient()

    def create_user(self):
        
        return CustomUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            cpf=self.cpf
        )

    def test_create_user(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "cpf": self.cpf
        }

       
        response = self.client.post(reverse('user-list'), user_data, format='json')

   
        assert response.status_code == 201
        assert CustomUser.objects.filter(username=self.username).exists()

        expected_message = f"O usuário {CustomUser.objects.get(username=self.username).user_id} - {self.username} foi registrado com sucesso."
        assert response.data["TicketGo"] == expected_message

    def test_login_user_fail(self):
    
        self.create_user()

      
        login_data = {
            "username": self.username,
            "password": "michael1"  
        }

      
        response = self.client.post(reverse('login'), login_data, format='json')

        assert response.status_code == 401
        assert "access_token" not in response.data
        assert "refresh_token" not in response.data


    def test_login_user_success(self):
      
        self.create_user()

        login_data = {
            "username": self.username,
            "password": self.password 
        }

        response = self.client.post(reverse('login'), login_data, format='json')

        assert response.status_code == 200
        assert "access_token" in response.data
        assert "refresh_token" in response.data
        assert response.data["user"]["username"] == self.username