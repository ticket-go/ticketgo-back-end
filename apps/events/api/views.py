from rest_framework import viewsets
from apps.events.api.serializers import EventsSerializer
from apps.events.models import Events

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    