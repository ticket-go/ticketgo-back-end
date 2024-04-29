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
    id_user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.id_user.username + " - " + str(self.value)

    def get_total_value(self):
        return sum(ticket.event.ticket_value for ticket in self.linked_purchase.all())
