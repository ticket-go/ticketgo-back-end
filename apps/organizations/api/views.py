from rest_framework import viewsets, permissions
from apps.organizations.api.serializers import OrganizationSerializer
from apps.events.models import Organization


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "uuid"
    # permission_classes = [permissions.IsAuthenticated]
