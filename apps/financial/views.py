import os

from apps.financial.filter import CartPaymentFilter
from dotenv import load_dotenv
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


from apps.financial.serializers import (
    CartPaymentSerializer,
    CreateInvoiceSerializer,
    ListPaymentsSerializer,
)
from apps.financial.asaas import AssasPaymentClient
from apps.financial.models import CartPayment

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions


load_dotenv()

ACCESS_TOKEN_ASASS = os.getenv("ASAAS_ACCESS_TOKEN")


class CartPaymentsViewSet(viewsets.ModelViewSet):
    queryset = CartPayment.objects.all()
    serializer_class = CartPaymentSerializer
    lookup_field = "uuid"
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = CartPaymentFilter

    def get_serializer_context(self):
        return {"request": self.request}

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def history(self, request, uuid=None):
        payment = self.get_object()
        history = payment.history.all()

        history_data = []
        for entry in history:
            if entry.prev_record:
                diff = entry.diff_against(entry.prev_record)
                changes = []
                for change in diff.changes:
                    field = CartPayment._meta.get_field(change.field)
                    verbose_name = field.verbose_name
                    changes.append(
                        {
                            "field": verbose_name,
                            "old_value": change.old,
                            "new_value": change.new,
                        }
                    )
            else:
                changes = "Initial creation"

            history_data.append(
                {
                    "history_id": entry.history_id,
                    "history_date": entry.history_date,
                    "history_change_reason": entry.history_change_reason,
                    "changes": changes,
                }
            )

        return Response(history_data)


class InvoicesAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ListPaymentsSerializer, responses={200: ListPaymentsSerializer}
    )
    def get(self, request):
        serializer = ListPaymentsSerializer(data=request.query_params)
        if serializer.is_valid():
            client = AssasPaymentClient()
            payments = client.list_payments()
            return Response(payments, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CreateInvoiceSerializer, responses={200: CreateInvoiceSerializer}
    )
    def post(self, request):
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            payment_uuid = serializer.validated_data["cart_payment"]
            payment = CartPayment.objects.get(uuid=payment_uuid)

            client = AssasPaymentClient()
            customer = client.create_or_update_customer(payment.user)
            data = self.prepare_payment_data(payment, customer)
            response = self.send_payment_request(data)

            if response:
                self.update_payment(payment, response)
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def prepare_payment_data(self, payment, customer):
        end_date = datetime.now() + timedelta(days=1)
        end_date_str = end_date.strftime("%Y-%m-%d")
        data = {
            "customer": customer.get("id"),
            "billingType": "UNDEFINED",
            "value": float(payment.value),
            "dueDate": end_date_str,
            "description": "Compre seus ingressos online de forma rápida e segura!",
            "externalReference": str(payment.uuid),
        }
        return data

    def send_payment_request(self, data):
        client = AssasPaymentClient()
        response = client.send_payment_request(data)

        return response

    def update_payment(self, payment, result):
        payment.link_payment = result["invoiceUrl"]
        payment.external_id = result["id"]
        payment.save()
