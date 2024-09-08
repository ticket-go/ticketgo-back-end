import os
from uuid import uuid4
from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator

from simple_history.models import HistoricalRecords

from apps.utils.cpf_cnpj.models import CNPJField, CPFField


def user_image_upload_to(instance, filename):
    return os.path.join(f"users/{instance.user_id}", filename)


class CustomUser(AbstractUser):
    GENDER_CHOICES = (("M", _("Homem")), ("F", _("Mulher")), ("O", _("Outro")))

    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    phone = models.CharField(max_length=12, verbose_name=_("Telefone"), null=True)
    cpf = CPFField(verbose_name=_("CPF"))
    cnpj = CNPJField(null=True, blank=True, verbose_name=_("CNPJ"))
    birthdate = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today)],
        verbose_name=_("Data de Nascimento"),
        default=date(2000, 1, 1),
    )
    image = models.ImageField(
        upload_to=user_image_upload_to, blank=True, verbose_name=_("Imagem do Usuário")
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Gênero"),
    )
    privileged = models.BooleanField(default=False, verbose_name=_("Privilegiado"))
    address = models.ForeignKey(
        "address.Address",
        related_name="user_address",
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("Endereço"),
    )
    history = HistoricalRecords()
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def get_user_id(self):
        return self.user_id

    def __str__(self):
        return self.username
