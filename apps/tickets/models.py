import hashlib

from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import BaseModel
from apps.financial.models import CartPayment
from apps.users.models import CustomUser
from apps.events.models import Event


class Ticket(BaseModel):
    verified = models.BooleanField(default=False, verbose_name=_("Verificado"))
    half_ticket = models.BooleanField(default=False, verbose_name=_("Meia-entrada"))
    hash = models.CharField(max_length=255, blank=True, null=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="linked_event",
        verbose_name=_("Evento"),
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="linked_user",
        verbose_name=_("Usuário"),
    )
    cart_payment = models.ForeignKey(
        CartPayment,
        on_delete=models.CASCADE,
        related_name="linked_card_payments",
        verbose_name=_("Compra"),
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.hash:
            hash_string = f"{self.id}-{self.event_id}-{self.user_id}"
            self.hash = hashlib.sha256(hash_string.encode()).hexdigest()
        super(Ticket, self).save(*args, **kwargs)
