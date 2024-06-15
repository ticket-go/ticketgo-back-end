from rest_framework import viewsets, permissions
from apps.events.api.serializers import EventsSerializer
from apps.events.models import Event


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    lookup_field = "uuid"
    permission_classes = [permissions.IsAuthenticated]

