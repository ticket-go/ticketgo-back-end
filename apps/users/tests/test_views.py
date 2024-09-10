import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import CustomUser
import uuid


@pytest.mark.django_db
class TestUserViews:
    username = "michael"
    email = "michael@michael.com"
    password = "michael"
    cpf = "12345678909"
    new_email = "michaelmichael@michael.com"
    privileged = False

    def setup_method(self):
        self.client = APIClient()

    def create_user(self, privileged=False, unique=False):
        if unique:
            username = f"{self.username}_{uuid.uuid4()}"
        else:
            username = self.username

        user = CustomUser.objects.create_user(
            username=username, email=self.email, password=self.password, cpf=self.cpf
        )
        user.privileged = privileged
        user.save()
        return user

    def test_create_user(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "cpf": self.cpf,
            "privileged": self.privileged,
        }

        response = self.client.post(
            reverse("customuser-list"), user_data, format="json"
        )

        assert response.status_code == 201
        assert CustomUser.objects.filter(username=self.username).exists()

        expected_message = f"O usuário {CustomUser.objects.get(username=self.username).user_id} - {self.username} foi registrado com sucesso."
        assert response.data["TicketGo"] == expected_message

    def test_login_user_fail(self):
        self.create_user()

        login_data = {"username": self.username, "password": "michael1"}

        response = self.client.post(reverse("login"), login_data, format="json")

        assert response.status_code == 401
        assert "access_token" not in response.data
        assert "refresh_token" not in response.data

    def test_login_user_success(self):
        self.create_user()

        login_data = {"username": self.username, "password": self.password}

        response = self.client.post(reverse("login"), login_data, format="json")

        assert response.status_code == 200
        assert "access_token" in response.data
        assert "refresh_token" in response.data
        assert response.data["user"]["username"] == self.username
        return response.data["access_token"]

    def test_logout_user_success(self):
        token = self.test_login_user_success()

        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(reverse("logout"))

        assert response.status_code == 200
        assert response.data["message"] == "Você foi desconectado com sucesso."

    def test_change_password_success(self):
        token = self.test_login_user_success()

        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        change_password_data = {
            "old_password": self.password,
            "new_password": "michael2",
            "confirm_new_password": "michael2",
        }

        response = self.client.put(
            reverse("change-password", args=[self.username]),
            change_password_data,
            format="json",
        )

        assert response.status_code == 200
        assert response.data["detail"] == "Senha alterada com sucesso."

        login_data = {"username": self.username, "password": "michael2"}

        login_response = self.client.post(reverse("login"), login_data, format="json")
        assert login_response.status_code == 200
        assert "access_token" in login_response.data

    def test_change_email_success(self):
        token = self.test_login_user_success()

        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        user_id = CustomUser.objects.get(username=self.username).user_id
        change_email_data = {"email": self.new_email}

        response = self.client.put(
            reverse("customuser-detail", args=[user_id]),
            change_email_data,
            format="json",
        )

        assert response.status_code == 200

        updated_user = CustomUser.objects.get(username=self.username)
        assert updated_user.email == self.new_email

    def test_login_mobile_success(self):
        self.create_user(privileged=True)

        login_data = {"username": self.username, "password": self.password}

        response = self.client.post(reverse("login-mobile"), login_data, format="json")

        assert response.status_code == 200
        assert "access_token" in response.data
        assert "refresh_token" in response.data
        assert response.data["user"]["username"] == self.username

    def test_login_mobile_no_permission(self):
        self.create_user(privileged=False)

        login_data = {"username": self.username, "password": self.password}

        response = self.client.post(reverse("login-mobile"), login_data, format="json")

        assert response.status_code == 401
        assert "access_token" not in response.data
        assert "refresh_token" not in response.data
        assert (
            response.data["error"]
            == "User does not have permission to access this application"
        )

    def test_delete_user_success(self):
        user = self.create_user(unique=True)
        user_id = user.user_id

        token = self.test_login_user_success()
        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(reverse("customuser-detail", args=[user_id]))

        assert response.status_code == 200
        assert (
            response.data["message"]
            == f"O usuário {user.username} foi desativado com sucesso."
        )

        user.refresh_from_db()
        assert user.is_active == False

    def test_partial_update_user_success(self):
        user = self.create_user(unique=True)
        token = self.test_login_user_success()
        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        user_id = user.user_id
        partial_update_data = {"first_name": "César"}

        response = self.client.patch(
            reverse("customuser-detail", args=[user_id]),
            partial_update_data,
            format="json",
        )

        assert response.status_code == 200
        assert response.data["first_name"] == "César"

        updated_user = CustomUser.objects.get(user_id=user_id)
        assert updated_user.first_name == "César"

    def test_list_users_success(self):
        self.create_user(unique=True)
        token = self.test_login_user_success()
        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(reverse("customuser-list"), format="json")

        assert response.status_code == 200
        assert len(response.data) > 0

    def test_retrieve_user_success(self):
        user = self.create_user(unique=True)
        token = self.test_login_user_success()
        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(
            reverse("customuser-detail", args=[user.user_id]), format="json"
        )
        assert response.status_code == 200
        assert response.data["username"] == user.username

    def test_user_history_success(self):
        user = self.create_user(unique=True)
        token = self.test_login_user_success()
        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(reverse("customuser-history"), format="json")

        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_change_email_already_exists(self):
        existing_user = CustomUser.objects.create_user(
            username="email",
            email="michael@michael.com",
            password=self.password,
            cpf="12345678901",
        )

        token = self.test_login_user_success()
        # Corrigindo o uso de HTTP_AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        user_id = CustomUser.objects.get(username=self.username).user_id
        change_email_data = {"email": "michael@michael.com"}

        response = self.client.put(
            reverse("customuser-detail", args=[user_id]),
            change_email_data,
            format="json",
        )

        assert response.status_code == 400
        assert "Este endereço de e-mail já está em uso" in response.data["error"]
