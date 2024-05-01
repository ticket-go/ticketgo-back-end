from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from apps.events.models import Event
from apps.tickets.models import Ticket
from apps.financial.models import Purchase
from apps.tickets.api.serializers import TicketSerializer


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        event = Event.objects.get(pk=event_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        half_ticket = serializer.validated_data.get("half_ticket", False)
        is_half_ticket = True if half_ticket else False

        # Check if there are available tickets for the event
        if event.tickets_available == 0:
            message = "Não há mais ingressos disponíveis para este evento."
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        if is_half_ticket and event.half_tickets_available == 0:
            message = "Não há mais ingressos do tipo meia-entrada disponíveis para este evento."
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        # Update the ticket count for the event
        if is_half_ticket:
            event.half_tickets_available -= 1
        else:
            event.tickets_available -= 1
        event.tickets_sold += 1
        event.save()

        # Check if there are half tickets for the event
        if not event.half_ticket_value:
            message = "Não há meia entrada disponível para este evento."
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

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
        event = instance.event

        # Update the ticket count for the event
        if instance.half_ticket:
            event.half_tickets_available += 1
        else:
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

    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<event_id>[^/.]+)/(?P<ticket_id>[^/.]+)/verify",
    )
    def verify(self, request, event_id=None, ticket_id=None):
        hash_value = request.data.get("hash")
        if not hash_value:
            return Response(
                {"error": "Hash not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        ticket = get_object_or_404(
            Ticket, id=ticket_id, event_id=event_id, hash=hash_value
        )

        if ticket.verified:
            return Response(
                {"message": "Ticket already verified"}, status=status.HTTP_200_OK
            )

        ticket.verified = True
        ticket.save()

        return Response(
            {"message": "Ticket verified successfully"}, status=status.HTTP_200_OK
        )
