from rest_framework import viewsets
from apps.address.api.serializers import AddressSerializer
from apps.address.models import Address


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
