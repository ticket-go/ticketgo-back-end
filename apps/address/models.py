from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.core.models import BaseModel


# Create your models here.
class Address(BaseModel):

    STATES_BR_CHOICES = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    )
    street = models.CharField(max_length=255, null=False, verbose_name=_("Rua"))
    number = models.IntegerField(null=False, verbose_name=_("Número"))
    district = models.CharField(max_length=255, null=False, verbose_name=_("Bairro"))
    city = models.CharField(max_length=255, null=False, verbose_name=_("Cidade"))
    state = models.CharField(
        max_length=255, null=False, choices=STATES_BR_CHOICES, verbose_name=_("Estado")
    )
    country = models.CharField(max_length=255, null=False, verbose_name=_("País"))
    zip_code = models.CharField(max_length=9, null=False, verbose_name=_("CEP"))
    complement = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Complemento")
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Address's ")

    def __str__(self):
        return self.street + " - " + self.district + " - " + self.state

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})
