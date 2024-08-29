from rest_framework import serializers
from apps.events.models import Event
from apps.address.models import Address
from apps.address.api.serializers import AddressSerializer
from apps.core.models import CustomUser
from apps.users.api.serializers import CustomUserSerializer
from drf_spectacular.utils import extend_schema_field


class EventsSerializer(serializers.ModelSerializer):
    address = serializers.UUIDField(write_only=True)
    address_data = AddressSerializer(source="address", read_only=True)
    user = CustomUserSerializer(read_only=True)
    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
    half_tickets_available = serializers.IntegerField(read_only=True)
    tickets_verified = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    category_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "uuid",
            "name",
            "date",
            "time",
            "description",
            "category",
            "category_display",
            "status",
            "status_display",
            "image",
            "image_url",
            "ticket_value",
            "half_ticket_value",
            "ticket_quantity",
            "half_ticket_quantity",
            "tickets_sold",
            "tickets_available",
            "half_tickets_available",
            "tickets_verified",
            "is_top_event",
            "is_hero_event",
            "address",
            "address_data",
            "user",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

    @extend_schema_field(serializers.CharField())
    def get_category_display(self, obj):
        return obj.get_category_display()

    @extend_schema_field(serializers.CharField())
    def get_status_display(self, obj):
        return obj.get_status_display()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context["request"].method in ["POST"]:
            self.fields["name"].required = True
            self.fields["date"].required = True
            self.fields["time"].required = True
            self.fields["category"].required = True
            self.fields["status"].required = True
            self.fields["image"].required = True
            self.fields["ticket_value"].required = True
            self.fields["ticket_quantity"].required = True
            self.fields["address"].required = True
        else:
            self.fields["name"].required = False
            self.fields["date"].required = False
            self.fields["time"].required = False
            self.fields["description"].required = False
            self.fields["category"].required = False
            self.fields["status"].required = False
            self.fields["image"].required = False
            self.fields["ticket_value"].required = False
            self.fields["ticket_quantity"].required = False
            self.fields["address"].required = False

    def create(self, validated_data):
        address = Address.objects.get(uuid=validated_data.pop("address"))
        user = self.context["request"].user

        event = Event.objects.create(address=address, user=user, **validated_data)
        return event

    def update(self, instance, validated_data):
        address = validated_data.pop("address", None)

        if address:
            instance.address = Address.objects.get(uuid=address)

        return super().update(instance, validated_data)
