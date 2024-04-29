from rest_framework import serializers
from apps.tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["half_ticket", "verified", "hash", "event", "user", "purchase"]

    hash = serializers.CharField(read_only=True)
