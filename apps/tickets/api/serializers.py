from apps.financial.models import CartPayment
from apps.users.api.serializers import CustomUserSerializer
from rest_framework import serializers
from apps.tickets.models import Ticket


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
        ]

    external_id = serializers.CharField(read_only=True)
    link_payment = serializers.CharField(read_only=True)
    payment_type = serializers.CharField(read_only=True)


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = [
            "uuid",
            "half_ticket",
            "verified",
            "hash",
            "user",
            "event",
            "cart_payment",
            "cart_payment_data",
        ]

    hash = serializers.CharField(read_only=True)
    verified = serializers.BooleanField(read_only=True)
    user = CustomUserSerializer(read_only=True)
    event = serializers.ReadOnlyField(source="event.uuid", read_only=True)
    cart_payment = serializers.UUIDField(write_only=True)
    cart_payment_data = serializers.SerializerMethodField(read_only=True)

    def get_cart_payment_data(self, obj):
        return CartPaymentSerializer(obj.cart_payment).data


class VerifyTicketSerializer(serializers.Serializer):
    hash = serializers.CharField()
