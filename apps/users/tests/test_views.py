import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
class TestUserViews:
    username = "michael"
    email = "michael@michael.com"
    password = "michael"
    cpf = "12345678909"
    new_email = "michaelmichael@michael.com"

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
        return response.data['access_token']

    
    def test_logout_user_success(self):
   
        token = self.test_login_user_success()

        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

 
        response = self.client.post(reverse('logout'))

  
        assert response.status_code == 200
        assert response.data["message"] == "Você foi desconectado com sucesso."



    def test_change_password_success(self):
            
            token = self.test_login_user_success()

            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

            change_password_data = {
                "old_password": self.password,
                "new_password": "michael2",
                "confirm_new_password": "michael2"
            }

    
            response = self.client.put(reverse('change-password', args=[self.username]), change_password_data, format='json')

    
            assert response.status_code == 200
            assert response.data["detail"] == "Senha alterada com sucesso."


            login_data = {
                "username": self.username,
                "password": "michael2"
            }

            login_response = self.client.post(reverse('login'), login_data, format='json')

            assert login_response.status_code == 200
            assert "access_token" in login_response.data
    
    def test_change_email_success(self):
       
        token = self.test_login_user_success()

        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

  
        user_id = CustomUser.objects.get(username=self.username).user_id
        change_email_data = {
            "email": self.new_email
        }

     
        response = self.client.put(reverse('user-detail', args=[user_id]), change_email_data, format='json')

       
        assert response.status_code == 200

        updated_user = CustomUser.objects.get(username=self.username)
        assert updated_user.email == self.new_email