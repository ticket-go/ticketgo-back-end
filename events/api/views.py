from rest_framework import viewsets
from events.api.serializers import EventsSerializer
from events.models import Events

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    