from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.address.models import Address
from apps.core.models import BaseModel


class Event(BaseModel):
    CATEGORY_GROUP_CHOICES = (
        ("music", _("Música")),
        ("sports", _("Esportes")),
        ("entertainment", _("Entretenimento")),
        ("conference", _("Conferência")),
        ("workshop", _("Workshop")),
        ("other", _("Outros")),
    )

    STATUS_GROUP_CHOICES = (
        ("scheduled", _("Agendado")),
        ("cancelled", _("Cancelado")),
        ("concluded", _("Concluído")),
    )

    name = models.CharField(
        _("Nome do evento"),
        max_length=255,
        null=False,
    )
    date = models.DateField(
        auto_now=False, auto_now_add=False, null=False, verbose_name=_("Data")
    )
    time = models.TimeField(
        auto_now=False, auto_now_add=False, null=False, verbose_name=_("Horário")
    )
    description = models.TextField(null=False, verbose_name=_("Descrição"))
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_GROUP_CHOICES,
        null=False,
        verbose_name=_("Categoria"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_GROUP_CHOICES,
        null=False,
        verbose_name=_("Status"),
    )
    image = models.ImageField(upload_to="events", null=False, verbose_name=_("Banner"))
    ticket_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Valor do ingresso")
    )
    half_ticket_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Meia entrada"),
        null=True,
        blank=True,
    )
    ticket_quantity = models.IntegerField(
        null=False, verbose_name=_("Quantidade de ingressos")
    )
    tickets_sold = models.IntegerField(
        default=0, verbose_name=_("Quantidade de ingressos vendidos")
    )
    tickets_available = models.IntegerField(
        null=False, verbose_name=_("Quantidade de ingressos disponíveis")
    )
    address = models.ForeignKey(
        Address,
        related_name="event_address",
        on_delete=models.CASCADE,
        verbose_name=_("Endereço"),
    )

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.tickets_available = self.ticket_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("events_detail", kwargs={"pk": self.pk})
