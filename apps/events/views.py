from apps.events.filter import EventFilter
from apps.events.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from apps.events.serializers import EventsSerializer
from apps.events.models import Event
from rest_framework.permissions import IsAuthenticated


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    lookup_field = "uuid"
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}

    