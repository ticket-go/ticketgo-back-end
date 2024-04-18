from rest_framework import viewsets
from apps.events.api.serializers import EventsSerializer
from apps.events.models import Event


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
