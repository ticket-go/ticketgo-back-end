from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.events.models import Event

from apps.tickets.api.serializers import TicketSerializer
from apps.tickets.models import Ticket


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        event = Event.objects.get(pk=event_id)

        if event.tickets_available == 0:
            return Response(
                {"error": "Não há mais ingressos disponíveis para este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event.tickets_available -= 1
        event.tickets_sold += 1
        event.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
