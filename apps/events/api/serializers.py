from rest_framework import serializers
from apps.events.models import Event


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "name",
            "date",
            "time",
            "description",
            "category",
            "status",
            "image",
            "ticket_value",
            "half_ticket_value",
            "ticket_quantity",
            "tickets_sold",
            "tickets_available",
            "address",
        ]

    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
