from rest_framework import viewsets
from apps.organizations.api.serializers import OrganizationSerializer
from apps.events.models import Organization


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
