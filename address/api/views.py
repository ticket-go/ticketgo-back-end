from rest_framework import viewsets
from address.api.serializers import AddressSerializer
from address.models import Address

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer