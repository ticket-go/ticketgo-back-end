from rest_framework import serializers
from apps.events.api.serializers import EventsSerializer
from apps.organizations.models import Organization
from apps.users.api.serializers import CustomUserUpdateSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    user_organization = CustomUserUpdateSerializer(many=True, read_only=True)
    event_organization = EventsSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ["uuid", "name", "cnpj", "user_organization", "event_organization"]
