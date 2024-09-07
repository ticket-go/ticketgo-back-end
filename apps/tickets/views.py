import os
import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from apps.financial.models import CartPayment
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action


from django.shortcuts import get_object_or_404

from apps.events.models import Event
from apps.tickets.models import Ticket
from apps.tickets.serializers import TicketSerializer, VerifyTicketSerializer


class TicketEmailService:

    def trigger_ticket_email(self, event_uuid, uuid):
        try:
            ticket = Ticket.objects.get(event__uuid=event_uuid, uuid=uuid)
            qr_img_bytes = self.generate_qr_code(ticket.hash)
            self.send_email_with_attachment(ticket, qr_img_bytes)
            print("Email enviado com sucesso!")
        except Ticket.DoesNotExist:
            raise Exception("Ticket não encontrado")

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
                <li><strong>Valor:</strong> R${ticket.cart_payment.value}</li>
                <li><strong>Data de compra:</strong> {ticket.cart_payment.created_at}</li>
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


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="event_uuid",
            type=str,
            description="UUID of the event",
            location=OpenApiParameter.PATH,
        ),
    ]
)
class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = "uuid"
    permission_classes = [permissions.IsAuthenticated]

    def get_event(self):
        event_pk = self.kwargs.get("event_uuid")
        return get_object_or_404(Event, uuid=event_pk)

    def get_payment(self):
        payment_pk = self.request.data.get("cart_payment")
        return get_object_or_404(CartPayment, uuid=payment_pk)

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

    @action(
        methods=["get"],
        detail=False,
        url_path="confirmed",
        url_name="confirmed",
    )
    def list_confirmed_tickets(self, request, event_uuid=None):
        try:
            event = Event.objects.get(uuid=event_uuid)
            confirmed_tickets = event.tickets.filter(cart_payment__status="RECEIVED")
            serializer = TicketSerializer(confirmed_tickets, many=True)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(
                {"error": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Ocorreu um erro inesperado. " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        event = self.get_event()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        half_ticket = serializer.validated_data.get("half_ticket", False)
        is_half_ticket = True if half_ticket else False

        print(f"Tickets available: {event.tickets_available}")
        if not is_half_ticket and event.tickets_available <= 0:
            message = "Não há mais ingressos disponíveis para este evento."
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        if is_half_ticket and event.half_tickets_available <= 0:
            message = "Não há mais ingressos do tipo meia-entrada disponíveis para este evento."
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        
        if is_half_ticket and event.half_ticket_quantity <= 0:
            message = "Não há meia-entrada disponível para este evento."
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

       
        if is_half_ticket:
            event.half_tickets_available -= 1
        else:
            event.tickets_available -= 1
        event.tickets_sold += 1
        event.save()

        payment = self.get_payment()

        ticket_value = event.half_ticket_value if is_half_ticket else event.ticket_value
        payment.value += ticket_value
        payment.save()

        serializer.validated_data["event"] = event
        serializer.validated_data["user"] = request.user
        serializer.validated_data["cart_payment"] = payment
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        event = instance.event

       
        if instance.half_ticket:
            event.half_tickets_available += 1
        else:
            event.tickets_available += 1
        event.tickets_sold -= 1
        event.save()

      
        payment = instance.cart_payment
        ticket_value = (
            instance.event.half_ticket_value
            if instance.half_ticket
            else instance.event.ticket_value
        )
        payment.value -= ticket_value
        payment.save()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyTicketViewSet(generics.UpdateAPIView):
    serializer_class = VerifyTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        event_uuid = kwargs.get("event_uuid")

        hash_value = request.data.get("hash")
        if not hash_value:
            return Response(
                {"error": "Hash não fornecida"}, status=status.HTTP_400_BAD_REQUEST
            )

        event = get_object_or_404(Event, uuid=event_uuid)
        ticket = get_object_or_404(Ticket, event=event, hash=hash_value)

        if ticket.verified:
            return Response(
                {
                    "message": "Este ingresso já foi verificado. Por favor, verifique outro ingresso ou entre em contato com o suporte se você achar que isso é um erro."
                },
                status=status.HTTP_409_CONFLICT,
            )

        ticket.verified = True
        ticket.save()

        return Response(
            {"message": "Ingresso verificado com sucesso!"}, status=status.HTTP_200_OK
        )
