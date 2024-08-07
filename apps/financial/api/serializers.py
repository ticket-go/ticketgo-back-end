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
    payment_type = serializers.CharField(read_only=True)
    purchase = serializers.CharField(source="purchase.uuid")

    def create(self, validated_data):
        purchase_uuid = validated_data.pop("purchase")
        purchase = Purchase.objects.get(uuid=purchase_uuid["uuid"])
        payment = Payment.objects.create(purchase=purchase, **validated_data)
        return payment


class CreateInvoiceSerializer(serializers.Serializer):
    payment = serializers.UUIDField()

    def validate_payment_id(self, value):
        try:
            payment = Payment.objects.get(uuid=value)
        except Payment.DoesNotExist:
            raise serializers.ValidationError("Pagamento não encontrado.")
        return payment


class ListPaymentsSerializer(serializers.Serializer):
    customer = serializers.CharField(required=False)


class AsaasCustomerSerializer(serializers.Serializer):
    externalReference = serializers.CharField(source="user_id")
    name = serializers.SerializerMethodField()
    cpfCnpj = serializers.CharField(source="cpf")
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.CharField(source="address.street")
    addressNumber = serializers.CharField(source="address.number")
    complement = serializers.CharField(source="address.complement")
    province = serializers.CharField(source="address.district")
    postalCode = serializers.CharField(source="address.zip_code")

    def get_name(self, obj):
        return obj.get_full_name()
