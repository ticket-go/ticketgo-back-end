import django_filters
from .models import Event


class EventFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category", lookup_expr="exact")

    class Meta:
        model = Event
        fields = ["category"]
