import os
import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from drf_spectacular.utils import extend_schema, OpenApiParameter

from config import settings
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action


from django.shortcuts import get_object_or_404

from apps.events.models import Event
from apps.tickets.models import Ticket
from apps.financial.models import Purchase
from apps.tickets.api.serializers import TicketSerializer, VerifyTicketSerializer


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = "uuid"
    # permission_classes = [permissions.IsAuthenticated]

    def get_event(self):
        event_pk = self.kwargs.get("event_uuid")
        return get_object_or_404(Event, uuid=event_pk)

    def get_purchase(self):
        purchase_pk = self.request.data.get("purchase")
        return get_object_or_404(Purchase, uuid=purchase_pk)

    def get_queryset(self):
        event_uuid = self.kwargs.get("event_uuid")
        event = get_object_or_404(Event, uuid=event_uuid)
        return Ticket.objects.filter(event=event)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="event_uuid",
                type=str,
                description="UUID of the event associated with the tickets",
                location=OpenApiParameter.PATH,
            )
        ],
        responses={200: TicketSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        event = self.get_event()

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

        purchase = self.get_purchase()
        # Update the purchase value
        half_ticket = serializer.validated_data.get("half_ticket", False)
        ticket_value = event.half_ticket_value if half_ticket else event.ticket_value
        purchase.value += ticket_value
        purchase.save()

        serializer.validated_data["event"] = event
        serializer.validated_data["user"] = request.user
        serializer.validated_data["purchase"] = purchase
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
        methods=["get"],
        detail=True,
        url_path="send-ticket-email",
        url_name="send_ticket_email",
    )
    def send_ticket_to_user_email(self, request, event_uuid=None, uuid=None):
        try:
            ticket = self.get_object()
            qr_img_bytes = self.generate_qr_code(ticket.hash)
            self.send_email_with_attachment(ticket, qr_img_bytes)
            return Response({"detail": "E-mail enviado com sucesso."})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def generate_qr_code(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white")

        qr_img_bytes = BytesIO()
        qr_img.save(qr_img_bytes)
        qr_img_bytes.seek(0)
        return qr_img_bytes

    def send_email_with_attachment(self, ticket, attachment):
        subject = "Seu ingresso está pronto! - TicketGO"
        message = f"""
        <html>
        <body>
            <h1>Olá, <strong>{ticket.user.username}</strong>!</h1>
            
            <p>Segue seu ingresso referente ao evento <strong>{ticket.event.name}</strong></p>

            <h3><strong>Detalhes do evento:</strong></h3>
            <ul>
                <li><strong>Data:</strong> {ticket.event.date}</li>
                <li><strong>Horário:</strong> {ticket.event.time}</li>
                <li><strong>Endereço:</strong> {ticket.event.address}</li>
            </ul>
            
            <h3><strong>Detalhes do ingresso:</strong></h3>
            <ul>
                <li><strong>ID:</strong> {ticket.uuid}</li>
                <li><strong>Valor:</strong> R${ticket.purchase.value}</li>
                <li><strong>Data de compra:</strong> {ticket.purchase.created_at}</li>
            </ul>
            
            <p>Anexado a este email, você encontrará o ingresso com o <strong>código QR</strong> que deverá ser apresentado na entrada do evento.</p>
            <p>Agradecemos pela sua compra e esperamos que você aproveite o evento!</p>

            <p>Atenciosamente,<br>
            Equipe <strong>TicketGO!</strong></p>
        </body>
        </html>
        """
        email = EmailMessage(
            subject, message, os.getenv("EMAIL_HOST_USER"), [ticket.user.email]
        )
        email.content_subtype = "html"
        email.attach("ticket_qr.png", attachment.read(), "image/png")
        email.send()


class VerifyTicketViewSet(generics.UpdateAPIView):
    serializer_class = VerifyTicketSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        event_uuid = kwargs.get("event_uuid")
        ticket_uuid = kwargs.get("ticket_uuid")

        hash_value = request.data.get("hash")
        if not hash_value:
            return Response(
                {"error": "Hash não fornecida"}, status=status.HTTP_400_BAD_REQUEST
            )

        event = get_object_or_404(Event, uuid=event_uuid)
        ticket = get_object_or_404(
            Ticket, uuid=ticket_uuid, event=event, hash=hash_value
        )

        if ticket.verified:
            return Response(
                {"message": "Ingresso já verificado!"}, status=status.HTTP_200_OK
            )

        ticket.verified = True
        ticket.save()

        return Response(
            {"message": "Ingresso verificado com sucesso!"}, status=status.HTTP_200_OK
        )
