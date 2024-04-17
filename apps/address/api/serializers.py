from rest_framework import serializers
from apps.address.models import Address

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['address_id', 'street', 'number', 'city', 'state', 'district', 'zip_code', 'country', 'complement']