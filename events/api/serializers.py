from rest_framework import serializers
from events.models import Events

class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['event_id', 'name_event', 'date', 'time', 'description', 'category', 'status', 'image', 'ticket_quantity', 'tickets_sold', 'tickets_available', 'address',]

    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)