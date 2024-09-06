import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import CustomUser

username = "michael"
email = "michael@michael.com"
password = "michael"
cpf = "12345678909"


@pytest.mark.django_db
def test_create_user():
    client = APIClient()
    
    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "cpf": cpf
    }
 
    response = client.post(reverse('user-list'), user_data, format='json')

    assert response.status_code == 201
    assert CustomUser.objects.filter(username=username).exists()

    assert "TicketGo" in response.data
    expected_message = f"O usuário {CustomUser.objects.get(username=username).user_id} - {username} foi registrado com sucesso."
    assert response.data["TicketGo"] == expected_message


@pytest.mark.django_db
def test_login_user_fail():
    client = APIClient()

    CustomUser.objects.create_user(
        username=username, 
        email=email, 
        password=password, 
        cpf=cpf
    )

    login_data = {
        "username": username,
        "password": "michael1"
    }

    response = client.post(reverse('login'), login_data, format='json')

    assert response.status_code == 401
    assert "access_token" not in response.data
    assert "refresh_token" not in response.data
