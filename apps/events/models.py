from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from apps.address.models import Address
from uuid import uuid4

class Events(models.Model):
    CATEGORY_GROUP_CHOICES = (
        ('music', _('Music')),
        ('sports', _('Sports')),
        ('entertainment', _('Entertainment')),
        ('conference', _('Conference')),
        ('workshop', _('Workshop')),
        ('other', _('Other')),
    )

    STATUS_GROUP_CHOICES = (
        ('pending', _('Pending')),
        ('scheduled', _('Scheduled')),
        ('cancelled', _('Cancelled')),
    )
    event_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name_event = models.CharField(_("Event Name"), max_length=255, null=False)
    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False, null=False)
    time = models.TimeField(_("Time"), auto_now=False, auto_now_add=False, null=False)
    description = models.TextField(_("Description"), null=False)
    category = models.CharField(_("Category"), max_length=50, choices=CATEGORY_GROUP_CHOICES, null=False)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_GROUP_CHOICES, null=False)
    image = models.ImageField(_("Image"), upload_to='media/events/{filename}', null=False)
    ticket_quantity = models.IntegerField(_("Ticket Quantity"), null=False)
    tickets_sold = models.IntegerField(_("Tickets Sold"), null=True, blank=True)
    tickets_available = models.IntegerField(_("Tickets Available"), null=True)
    address = models.ForeignKey(Address, related_name='event_address', on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.name_event

    def get_absolute_url(self):
        return reverse("events_detail", kwargs={"pk": self.pk})
