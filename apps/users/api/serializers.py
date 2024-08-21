from apps.address.api.serializers import AddressSerializer
from apps.address.models import Address
from rest_framework import serializers
from apps.users import models


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), required=False
    )

    class Meta:
        model = models.CustomUser
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "phone",
            "birthdate",
            "cpf",
            "email",
            "gender",
            "privileged",
            "address",
            "address_id",
            "password",
        ]
        read_only_fields = ["user_id"]

    def __init__(self, *args, **kwargs):
        context = kwargs.get("context", {})
        request = context.get("request", None)
        super().__init__(*args, **kwargs)
        if request and request.method in ["POST"]:
            self.fields["username"].required = True
            self.fields["cpf"].required = True
            self.fields["password"].required = True
        else:
            self.fields["username"].required = False
            self.fields["cpf"].required = False
            self.fields["password"].required = False

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        address_data = validated_data.pop("address_id", None)

        user = super().create(validated_data)
        if password:
            user.set_password(password)
        if address_data:
            user.user_address = address_data
        user.save()
        return user

    def update(self, instance, validated_data):
        adress_data = validated_data.pop("address_id", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if adress_data is not None:
            instance.user_address = adress_data
        instance.save()
        return instance


class CustomUserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context["request"].user
        if not user.check_password(data.get("old_password")):
            print(f"Senha antiga fornecida: {data.get('old_password')}")
            print(f"Senha atual do usuário: {user.password}")
            raise serializers.ValidationError(
                {"old_password": "Senha antiga incorreta."}
            )
        if data.get("new_password") != data.get("confirm_new_password"):
            raise serializers.ValidationError(
                {"new_password": "As novas senhas não coincidem."}
            )
        return data


class CustomUserChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=16)
