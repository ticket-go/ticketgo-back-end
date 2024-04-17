from django.db import models
from address.models import Address
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    phone = models.CharField(max_length=12, blank=True)
    cpf = models.CharField(max_length=11, blank=True)
    #birth = models.DateField(blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Homem'), ('F', 'Mulher'), ('O', 'Outro')], blank=True)
    privileged = models.BooleanField(default=False)  
    address = models.ForeignKey(Address, related_name='user_address', on_delete=models.SET_NULL, null=True, blank=True)

    def get_user_id(self):
        return self.user_id