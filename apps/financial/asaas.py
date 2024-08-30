import os
import requests
import schedule
import threading
import time

from requests import HTTPError
from dotenv import load_dotenv
from functools import partialmethod

from apps.financial.models import CartPayment
from .serializers import AsaasCustomerSerializer


load_dotenv()


ASAAS_ENDPOINT_URL = "https://sandbox.asaas.com/api/v3"


class AssasPaymentClient:
    error_msgs = {
        400: "Envio de dados inválidos",
        401: "Chave de API inválida",
        500: "Erro no servidor",
    }

    def __init__(self, **kwargs):
        self.endpoint_url = ASAAS_ENDPOINT_URL
        self.request_headers = {
            "access_token": os.getenv("ASAAS_ACCESS_TOKEN"),
            "accept": "application/json",
            "content-type": "application/json",
        }

    def _request(self, method, url, **kwargs):
        response = requests.request(
            method,
            self.endpoint_url + url,
            headers=self.request_headers,
            **kwargs,
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise HTTPError(
                self.error_msgs.get(response.status_code, "Erro desconhecido"),
                response=self,
            )

        return response.json()

    _api_get = partialmethod(_request, "get")
    _api_put = partialmethod(_request, "put")
    _api_post = partialmethod(_request, "post")

    def create_or_update_customer(self, user, **kwargs):
        customer_id = self._get_customer_id(user.cpf)
        customer_data = AsaasCustomerSerializer(user).data
        if customer_id:
            response = self._update_customer(customer_id, customer_data)
            return response
        else:
            response = self._create_customer(customer_data)
            return response

    def _get_customer_id(self, cpf):
        response = self._api_get(f"/customers?cpfCnpj={cpf}")
        if response["totalCount"] > 0:
            customer_id = response["data"][0]["id"]
            return customer_id
        return None

    def _update_customer(self, customer_id, data):
        return self._api_put(f"/customers/{customer_id}", json=data)

    def _create_customer(self, data):
        return self._api_post("/customers", json=data)

    def send_payment_request(self, data):
        return self._api_post("/payments", json=data)

    def list_payments(self, data=None):
        if data:
            return self._api_get("/payments", json=data)
        return self._api_get("/payments")

    def check_payment_status(self):
        response = self._api_get("/payments")
        all_payments = response["data"]
        for payment in all_payments:
            try:
                existing_payment = CartPayment.objects.get(external_id=payment["id"])
                existing_payment.status = payment["status"]
                existing_payment.payment_type = payment["billingType"]
                existing_payment.save()
            except CartPayment.DoesNotExist:
                pass


# # polling status check payments

# client = AssasPaymentClient()


# def check_payments():
#     schedule.every(1).minutes.do(client.check_payment_status)


# check_payments()


# # to run in the background
# def schedule_thread():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# # config to run in the background
# threading.Thread(target=schedule_thread).start()
