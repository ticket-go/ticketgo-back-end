from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect

from rest_framework import generics, status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.api import serializers
from apps.users.models import CustomUser

CustomUser = get_user_model()


class UserViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.CustomUserUpdateSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "user_id"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        new_email = serializer.validated_data.get("email", None)

        if new_email and CustomUser.objects.filter(email=new_email).exists():
            return Response(
                {"error": "Este endereço de e-mail já está em uso por outro usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_update(serializer)

        return Response(serializer.data)


class CustomUserViewSet(generics.CreateAPIView):

    serializer_class = serializers.CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email", None)
            if email and CustomUser.objects.filter(email=email).exists():
                return Response(
                    {
                        "error": "Este endereço de e-mail já está em uso por outro usuário."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = CustomUser.objects.create_user(
                username=serializer.validated_data.get("username"),
                cpf=serializer.validated_data.get("cpf"),
                email=serializer.validated_data.get("email"),
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                phone=serializer.validated_data.get("phone"),
                birthdate=serializer.validated_data.get("birthdate"),
                gender=serializer.validated_data.get("gender"),
                address=serializer.validated_data.get("address"),
                privileged=serializer.validated_data.get("privileged"),
                password=serializer.validated_data.get("password"),
            )

            return Response(
                {"TicketGo": f"O usuário {user.username} foi registrado com sucesso."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserChangePasswordViewSet(generics.UpdateAPIView):

    serializer_class = serializers.CustomUserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.CustomUserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            if not check_password(old_password, user.password):
                return Response(
                    {"error": "A senha antiga fornecida está incorreta."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):

    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                try:
                    access_token = RefreshToken.for_user(user)
                except TokenError as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                return Response(
                    {
                        "access_token": str(access_token.access_token),
                        "refresh_token": str(access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"message": "Você foi desconectado com sucesso."}, status=status.HTTP_200_OK
        )


class SocialLoginViewSet(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None

    def get(self, request, *args, **kwargs):
        provider = kwargs.get("provider")

        if provider == "google":
            # Redirecionar para a página de login social do provedor do Google
            return redirect("/accounts/google/login/")
        else:
            return Response({"error": "Provider not supported"}, status=400)
