from rest_framework import serializers
from users import models



#Dados do usuário

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = '__all__'

    def create_user(self, validated_data):
        
        user = models.CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
           
        )
        return user

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'phone', 'gender', 'address']





#Autenticação

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=16)
