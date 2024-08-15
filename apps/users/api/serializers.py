from apps.address.models import Address
from apps.organizations.models import Organization
from rest_framework import serializers
from apps.users import models


# Dados do usuário
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    address = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Address.objects.all(), required=False
    )
    organization = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Organization.objects.all(), required=False
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
            "organization",
            "password",
        ]
        read_only_fields = ["user_id"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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
