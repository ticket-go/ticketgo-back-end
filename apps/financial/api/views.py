import os
import requests

from dotenv import load_dotenv
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema

from apps.financial.api.serializers import (
    CreatePaymentLinkSerializer,
    PaymentSerializer,
    PurchaseSerializer,
)
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


class GeneratePaymentLinkAPIView(APIView):
    @extend_schema(request=CreatePaymentLinkSerializer)
    def post(self, request):
        serializer = CreatePaymentLinkSerializer(data=request.data)
        if serializer.is_valid():
            payment_uuid = serializer.validated_data["payment"]
            payment = Payment.objects.get(uuid=payment_uuid)

            url = "https://sandbox.asaas.com/api/v3/paymentLinks"
            headers = {
                "Content-Type": "application/json",
                "access_token": ACCESS_TOKEN_ASASS,
            }

            max_installment_count = 0
            if payment.purchase.value > 50 and payment.purchase.value < 100:
                max_installment_count = 2
            elif payment.purchase.value > 10 and payment.purchase.value < 200:
                max_installment_count = 4
            else:
                max_installment_count = 5

            end_date = datetime.now() + timedelta(days=1)
            end_date_str = end_date.strftime("%Y-%m-%d")

            data = {
                "name": "Venda de tickets - TicketGo",
                "description": "Compre seus ingressos online de forma rápida e segura! Não perca tempo, garanta seus ingressos agora! ",
                "value": float(payment.purchase.value),
                "billingType": payment.payment_type,
                "chargeType": (
                    "DETACHED" if payment.payment_type == "PIX" else "INSTALLMENT"
                ),
                "dueDateLimitDays": 1,
                "maxInstallmentCount": max_installment_count,
                "endDate": end_date_str,
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                link_payment = result["url"]
                external_id = result["id"]

                payment.link_payment = link_payment
                payment.external_id = external_id
                payment.save()

                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
