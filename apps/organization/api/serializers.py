from rest_framework import serializers
from apps.organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'company_regisration_number', 'event_organization']