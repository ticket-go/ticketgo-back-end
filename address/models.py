from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from uuid import uuid4

# Create your models here.
class Address(models.Model):

    STATES_BR_CHOICES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )
    address_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    street = models.CharField(_("Street"), max_length=255, null=False)
    number = models.IntegerField(_("Number"), null=False)
    district = models.CharField(_("District"), max_length=255, null=False)
    city = models.CharField(_("City"), max_length=255, null=False)
    state = models.CharField(_("State"), max_length=255, null=False,choices=STATES_BR_CHOICES)
    country = models.CharField(_("Country"), max_length=255, null=False)
    zip_code = models.CharField(_("Zip Code"), max_length=9, null=False)
    complement = models.CharField(_("Complement"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Address's ")

    def __str__(self):
        return self.street

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})
