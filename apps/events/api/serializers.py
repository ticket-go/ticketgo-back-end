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
            "category_display",
            "status",
            "status_display",
            "image",
            "ticket_value",
            "half_ticket_value",
            "ticket_quantity",
            "half_ticket_quantity",
            "tickets_sold",
            "tickets_available",
            "half_tickets_available",
            "address",
            "organization",
        ]

    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
    half_tickets_available = serializers.IntegerField(read_only=True)
    category_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    def get_category_display(self, obj):
        return obj.get_category_display()

    def get_status_display(self, obj):
        return obj.get_status_display()
