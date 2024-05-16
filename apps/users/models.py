from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext as _

from django.core.validators import MaxValueValidator

from uuid import uuid4

from apps.utils.cpf_cnpj.models import CPFField


class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    phone = models.CharField(max_length=12, verbose_name=_("Telefone"))
    cpf = CPFField(verbose_name=_("CPF"))
    birthdate = models.DateField(
        null=True,
        validators=[MaxValueValidator(limit_value=date.today)],
        verbose_name=_("Data de Nascimento"),
    )
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Homem"), ("F", "Mulher"), ("O", "Outro")],
        blank=True,
        verbose_name=_("Gênero"),
    )
    privileged = models.BooleanField(default=False, verbose_name=_("Privilegiado"))
    address = models.ForeignKey(
        "address.Address",
        related_name="user_address",
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name=_("Endereço"),
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        verbose_name=_("Organização"),
        related_name="user_organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def get_user_id(self):
        return self.user_id
