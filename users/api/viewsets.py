from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.api import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import Token, RefreshToken, TokenError
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from users.api import serializers

class CustomUserViewSet(generics.CreateAPIView):

    serializer_class = serializers.CustomUserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            
            password = serializer.validated_data.get('password')
            
            user = serializer.create_user(serializer.validated_data)
            
            return Response({'TicketGo': f'O usuário {user.username} foi registrado com sucesso.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserUpdateViewSet(generics.UpdateAPIView):
    serializer_class = serializers.CustomUserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Seus dados foram editados com sucesso.'}, status=status.HTTP_200_OK)

class LoginViewSet(APIView):

    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                try:
                    access_token = RefreshToken.for_user(user)
                except TokenError as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'access_token': str(access_token.access_token), 'refresh_token': str(access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
