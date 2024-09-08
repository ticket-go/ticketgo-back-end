import django_filters
from .models import CartPayment


class CartPaymentFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name="user", lookup_expr="exact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = CartPayment
        fields = [
            "user",
            "status",
        ]
