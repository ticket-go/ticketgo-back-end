from rest_framework import serializers
from apps.financial.models import Purchase
from apps.tickets.api.serializers import TicketSerializer


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ["uuid", "value", "status", "id_user", "tickets"]

    tickets = TicketSerializer(many=True, read_only=True)
