from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.core.models import BaseModel
# Create your models here.

class Payment(BaseModel):
    STATUS_CHOICES = (
        ("approved", _("Approved")),
        ("pending", _("Pending")),
        ("in_process", _("In process")),
        ("rejected", _("Rejected")),
        ("cancelled", _("Cancelled")),
        ("refunded", _("Refunded")),
        ("charged_back", _("Charged back")),
    )
    token = models.CharField(max_length=100)
    transaction_amount = models.FloatField()
    installments = models.IntegerField()
    payment_method_id = models.CharField(max_length=100)
    issuer_id = models.CharField(max_length=100, blank=True, null=True)
    payer_first_name = models.CharField(max_length=100)
    payer_email = models.EmailField()
    payer_identification_type = models.CharField(max_length=100)
    payer_identification_number = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="pending")
    status_detail = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

    def get_absolute_url(self):
        return reverse("payments:payment-detail", kwargs={"pk": self.pk})