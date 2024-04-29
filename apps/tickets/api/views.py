from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.events.models import Event

from apps.financial.models import Purchase
from apps.tickets.api.serializers import TicketSerializer
from apps.tickets.models import Ticket


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        event = Event.objects.get(pk=event_id)

        # Check if there are available tickets for the event
        if event.tickets_available == 0:
            return Response(
                {"error": "Não há mais ingressos disponíveis para este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the ticket count for the event
        event.tickets_available -= 1
        event.tickets_sold += 1
        event.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if there are half tickets for the event
        if not event.half_ticket_value:
            return Response(
                {"error": "Não há meia entrada disponível para este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase_id = request.data.get("purchase")
        purchase = Purchase.objects.get(pk=purchase_id)

        # Update the purchase value
        half_ticket = serializer.validated_data.get("half_ticket", False)
        ticket_value = event.half_ticket_value if half_ticket else event.ticket_value
        purchase.value += ticket_value
        purchase.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Update the ticket count for the event
        event = instance.event
        event.tickets_available += 1
        event.tickets_sold -= 1
        event.save()

        # Update the purchase value
        purchase = instance.purchase
        ticket_value = (
            instance.event.half_ticket_value
            if instance.half_ticket
            else instance.event.ticket_value
        )
        purchase.value -= ticket_value
        purchase.save()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
