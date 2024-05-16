from rest_framework import serializers
from apps.financial.models import Purchase
from apps.tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = [
            "uuid",
            "half_ticket",
            "verified",
            "hash",
            "user",
            "event",
            "purchase",
        ]

    hash = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.ReadOnlyField(source="event.uuid", read_only=True)
    purchase = serializers.CharField()


class VerifyTicketSerializer(serializers.Serializer):
    hash = serializers.CharField()
