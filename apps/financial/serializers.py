from apps.users.serializers import CustomUserSerializer
from rest_framework import serializers
from apps.financial.models import CartPayment
from drf_spectacular.utils import extend_schema_field


class CartPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartPayment
        fields = [
            "uuid",
            "value",
            "status",
            "external_id",
            "payment_type",
            "status",
            "link_payment",
            "user",
            "user_data",
            "tickets",
        ]

    external_id = serializers.CharField(read_only=True)
    link_payment = serializers.CharField(read_only=True)
    payment_type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    value = serializers.CharField(read_only=True)
    user = serializers.UUIDField(read_only=True)
    tickets = serializers.SerializerMethodField(read_only=True)
    user_data = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(CustomUserSerializer)
    def get_user_data(self, obj):
        return CustomUserSerializer(obj.user).data

    def get_tickets(self, obj):
        uuid_tickets = obj.tickets.values_list("uuid", flat=True)
        return uuid_tickets

    def validate_payment_type(self, value):
        valid_types = ["CARD", "CASH", "PIX"]
        if value not in valid_types:
            raise serializers.ValidationError("Tipo de pagamento inválido.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        cart_payment = CartPayment.objects.create(user=user, **validated_data)
        return cart_payment


class CreateInvoiceSerializer(serializers.Serializer):
    cart_payment = serializers.UUIDField()

    def validate_cart_payment_id(self, value):
        try:
            cart_payment = CartPayment.objects.get(uuid=value)
        except CartPayment.DoesNotExist:
            raise serializers.ValidationError("Compra não encontrada.")
        return cart_payment


class ListPaymentsSerializer(serializers.Serializer):
    customer = serializers.CharField(required=False)


class AsaasCustomerSerializer(serializers.Serializer):
    externalReference = serializers.CharField(source="user_id")
    name = serializers.SerializerMethodField()
    cpfCnpj = serializers.CharField(source="cpf")
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.SerializerMethodField()
    addressNumber = serializers.CharField(source="address.number")
    complement = serializers.CharField(source="address.complement")
    province = serializers.CharField(source="address.district")
    postalCode = serializers.CharField(source="address.zip_code")

    def get_name(self, obj):
        return obj.get_full_name()

    def get_address(self, obj):
        if obj.address:
            return obj.address.street
        raise serializers.ValidationError(
            {"error": "Endereço não cadastrado para o usuário."}
        )
