from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.core.models import BaseModel
from apps.utils.cpf_cnpj.models import CNPJField


# Create your models here.
class Organization(BaseModel):

    name = models.CharField(max_length=255, null=False, verbose_name=_("Nome"))
    cnpj = CNPJField(null=False, blank=False, verbose_name=_("CNPJ"))

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Organization_detail", kwargs={"pk": self.pk})

    def get_events(self):
        return self.event_organization.all()
