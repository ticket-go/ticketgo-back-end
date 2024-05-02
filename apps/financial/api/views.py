from rest_framework import viewsets

from apps.financial.api.serializers import PurchaseSerializer
from apps.financial.models import Purchase


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = "uuid"
