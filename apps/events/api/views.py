from apps.events.filter import EventFilter
from apps.events.permissions import AllowListOnly
from rest_framework import viewsets, permissions
from apps.events.api.serializers import EventsSerializer
from apps.events.models import Event


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    lookup_field = "uuid"
    filterset_class = EventFilter
    permission_classes = [AllowListOnly]
