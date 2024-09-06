import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import CustomUser

@pytest.mark.django_db
def test_create_user():
    client = APIClient()

    username = "michael"
    
    user_data = {
        "username": username,
        "email": "newuser@example.com",
        "password": "password123",
        "cpf": "12345678909"
    }
 
    response = client.post(reverse('user-list'), user_data, format='json')

    assert response.status_code == 201
    assert CustomUser.objects.filter(username=username).exists()

    assert "TicketGo" in response.data
    expected_message = f"O usuário {CustomUser.objects.get(username=username).user_id} - {username} foi registrado com sucesso."
    assert response.data["TicketGo"] == expected_message
