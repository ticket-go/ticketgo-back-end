from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
import mercadopago
import json

from ..utils.mercadopago.init_point import generate_payment_link
from .models import Payment
# Create your views here.

class PaymentAPIView(APIView, View):
    permissions_classes = [permissions.IsAuthenticated] 


    def post(self, request):
        try:
            request = json.loads(request.body)
            default_values = {
                "transaction_amount": 10.0,  # Valor padrão da transação
                "installments": 1,  # Número padrão de parcelas
                "payment_method_id": "Mastercard",  # Método de pagamento padrão
                "issuer_id": None,  # ID do emissor padrão (opcional)
            }
            request_values = {**default_values, **request}
            payment_data = {
                "transaction_amount": float(request_values["transaction_amount"]),
                "token": request_values["token"],
                "installments": int(request_values["installments"]),
                "payment_method_id": request_values["payment_method_id"],
                "issuer_id": request_values["issuer_id"],
                "payer": {
                    "first_name": request_values["payer"]["first_name"],
                    "email": request_values["payer"]["email"],
                    "identification": {
                        "type": request_values["payer"]["identification"]["type"],
                        "number": request_values["payer"]["identification"]["number"],
                    },
                },
                "back_urls": {
                    "success": "http://127.0.0.1:8000/",
                    "pending": "http://test.com/pending",
                    "failure": "http://test.com/failure"
                },
                "auto_return": "all",
            }
            sdk = mercadopago.SDK(access_token=str(settings.ACCESS_TOKEN))
            payment_response = sdk.preference().create(payment_data)
            payment = payment_response["response"]
            status = {
                "id": payment["id"],
                "status": payment["status"],
                "status_detail": payment["status_detail"],
            }

            Payment.objects.create(
                token=payment_data["token"],
                transaction_amount=payment_data["transaction_amount"],
                installments=payment_data["installments"],
                payment_method_id=payment_data["payment_method_id"],
                issuer_id=payment_data.get("issuer_id"),
                payer_first_name=payment_data["payer"]["first_name"],
                payer_email=payment_data["payer"]["email"],
                payer_identification_type=payment_data["payer"]["identification"]["type"],
                payer_identification_number=payment_data["payer"]["identification"]["number"],
                status=status["status"],
                status_detail=status["status_detail"]
            )
            payment_link = generate_payment_link()

            response_data = {
                "body": status,
                "statusCode": payment_response["status"],
                "payment_link": payment_link  # Adicionando o link de pagamento à resposta
            }

            return Response(data=response_data, status=201)
        
        except Exception as error:
            return Response(data={"error": str(error)}, status=400)
        
def test(request):
    link = generate_payment_link()
    return render(request, "payments/process_payment.html", {"link": link})
        
