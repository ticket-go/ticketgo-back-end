from rest_framework import serializers
from apps.users import models


# Dados do usuário
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = "__all__"

    def create_user(self, validated_data):

        user = models.CustomUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class CustomUserUpdateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(read_only=True)

    class Meta:
        model = models.CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone",
            "email",
            "gender",
            "privileged",
            "address",
            "organization",
        ]

        extra_kwargs = {field: {"required": False} for field in fields}

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr != "email":
                setattr(instance, attr, value)
        instance.save()
        return instance


class CustomUserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):

        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("Senhas diferentes. Tente novamente.")
        return data


class CustomUserChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=16)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "cpf",
            "birthdate",
            "gender",
            "privileged",
            "address",
            "organization",
        ]
