from django.conf import settings
import mercadopago

def generate_payment_link():
    sdk = mercadopago.SDK(access_token=str(settings.ACCESS_TOKEN))
    payment_data = {
        "items": [
            {
                "id": "1234",
                "title": "Product",
                "description": "Description",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 100.00,
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:8000/payments/",
            "pending": "http://test.com/pending",
            "failure": "http://test.com/failure"
        },
        "auto_return": "all",
    }
    payment_response = sdk.preference().create(payment_data)
    payment = payment_response["response"]
    print(payment)
    init_point = payment["init_point"]

    return init_point