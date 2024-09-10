from apps.events.filter import EventFilter
from apps.events.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from apps.events.serializers import EventsSerializer
from apps.events.models import Event
from rest_framework.pagination import PageNumberPagination


class EventPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    lookup_field = "uuid"
    filterset_class = EventFilter
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = EventPagination

    def get_serializer_context(self):
        return {"request": self.request}

    