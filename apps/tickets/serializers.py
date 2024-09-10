from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.address.serializers import AddressSerializer
from apps.events.models import Event
from apps.financial.models import CartPayment
from apps.users.serializers import CustomUserSerializer
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


class EventsSerializer(serializers.ModelSerializer):
    address = serializers.UUIDField(write_only=True)
    address_data = AddressSerializer(source="address", read_only=True)
    user = CustomUserSerializer(read_only=True)
    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
    half_tickets_available = serializers.IntegerField(read_only=True)
    tickets_verified = serializers.IntegerField(read_only=True)
    category_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "uuid",
            "name",
            "date",
            "time",
            "description",
            "category",
            "category_display",
            "status",
            "status_display",
            "ticket_value",
            "half_ticket_value",
            "ticket_quantity",
            "half_ticket_quantity",
            "tickets_sold",
            "tickets_available",
            "half_tickets_available",
            "tickets_verified",
            "is_top_event",
            "is_hero_event",
            "address",
            "address_data",
            "user",
        ]

    @extend_schema_field(serializers.CharField())
    def get_category_display(self, obj):
        return obj.get_category_display()

    @extend_schema_field(serializers.CharField())
    def get_status_display(self, obj):
        return obj.get_status_display()


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
            "event_data",
            "cart_payment",
            "cart_payment_data",
        ]

    hash = serializers.CharField(read_only=True)
    half_ticket = serializers.BooleanField(required=False)
    verified = serializers.BooleanField(read_only=True)
    user = CustomUserSerializer(read_only=True)
    event = serializers.ReadOnlyField(source="event.uuid", read_only=True)
    event_data = serializers.SerializerMethodField(read_only=True)
    cart_payment = serializers.UUIDField(write_only=True)
    cart_payment_data = serializers.SerializerMethodField(read_only=True)

    def get_cart_payment_data(self, obj):
        return CartPaymentSerializer(obj.cart_payment).data

    def get_event_data(self, obj):
        return EventsSerializer(obj.event).data


class VerifyTicketSerializer(serializers.Serializer):
    hash = serializers.CharField()
