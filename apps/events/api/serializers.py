from apps.address.api.serializers import AddressSerializer
from apps.organizations.models import Organization
from apps.users.api.serializers import CustomUserSerializer
from rest_framework import serializers
from apps.events.models import Event
from drf_spectacular.utils import extend_schema_field


class OrganizationSerializer(serializers.ModelSerializer):
    user_organization = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ["uuid", "name", "cnpj", "user_organization"]


class EventsSerializer(serializers.ModelSerializer):

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
            "image",
            "ticket_value",
            "half_ticket_value",
            "ticket_quantity",
            "half_ticket_quantity",
            "tickets_sold",
            "tickets_available",
            "half_tickets_available",
            "tickets_verified",
            "address",
            "organization",
        ]

    address = AddressSerializer()
    organization = OrganizationSerializer()
    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
    half_tickets_available = serializers.IntegerField(read_only=True)
    tickets_verified = serializers.IntegerField(read_only=True)
    category_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_category_display(self, obj):
        return obj.get_category_display()

    @extend_schema_field(serializers.CharField())
    def get_status_display(self, obj):
        return obj.get_status_display()
