from rest_framework import serializers
from apps.financial.models import Payment, Purchase
from apps.tickets.api.serializers import TicketSerializer


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ["uuid", "value", "status", "user", "tickets"]

    tickets = TicketSerializer(many=True, read_only=True)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "uuid",
            "external_id",
            "payment_type",
            "status",
            "link_payment",
            "purchase",
        ]

    external_id = serializers.CharField(read_only=True)
    link_payment = serializers.CharField(read_only=True)


class CreatePaymentLinkSerializer(serializers.Serializer):
    payment = serializers.UUIDField()

    def validate_payment_id(self, value):
        try:
            payment = Payment.objects.get(uuid=value)
        except Payment.DoesNotExist:
            raise serializers.ValidationError("Pagamento não encontrado.")
        return payment
