import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema

from apps.financial.api.serializers import (
    CreateInvoiceSerializer,
    ListPaymentsSerializer,
    PaymentSerializer,
    PurchaseSerializer,
)
from apps.financial.asaas import AssasPaymentClient
from apps.financial.models import Payment, Purchase

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets


load_dotenv()

ACCESS_TOKEN_ASASS = os.getenv("ASAAS_ACCESS_TOKEN")


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = "uuid"


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class InvoicesAPIView(APIView):

    @extend_schema(request=ListPaymentsSerializer)
    def get(self, request):
        serializer = ListPaymentsSerializer(data=request.query_params)
        if serializer.is_valid():
            customer = serializer.validated_data.get("customer")
            client = AssasPaymentClient()
            if customer:
                data = {"customer": customer}
                payments = client.list_payments(data)
                return Response(payments, status=status.HTTP_200_OK)
            else:
                payments = client.list_payments()
                return Response(payments, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=CreateInvoiceSerializer)
    def post(self, request):
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            payment_uuid = serializer.validated_data["payment"]
            payment = Payment.objects.get(uuid=payment_uuid)

            client = AssasPaymentClient()
            customer = client.create_or_update_customer(payment.purchase.user)
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
            "value": float(payment.purchase.value),
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
