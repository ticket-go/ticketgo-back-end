from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import BaseModel
from apps.users.models import CustomUser


class Purchase(BaseModel):
    STATUS_GROUP_CHOICES = (
        ("pending", _("Aguardando pagamento")),
        ("completed", _("Pagamento concluído")),
    )

    value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Valor total"), default=0
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_GROUP_CHOICES,
        null=False,
        verbose_name=_("Status"),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.user.username + " - " + str(self.value)

    def get_total_value(self):
        return sum(ticket.event.ticket_value for ticket in self.linked_purchase.all())


class Payment(BaseModel):
    PAYMENT_STATUS_CHOICES = (
        ("PENDING", _("Pendente")),
        ("RECEIVED", _("Recebido")),
        ("CONFIRMED", _("Confirmado")),
    )

    external_id = models.CharField(
        max_length=50,
        editable=False,
        verbose_name=_("ID externo"),
        null=True,
        blank=True,
    )
    payment_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Tipo do pagamento"),
    )
    status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING",
        verbose_name=_("Status"),
    )
    link_payment = models.CharField(
        max_length=500, verbose_name=_("Link do pagamento"), null=True, blank=True
    )
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
