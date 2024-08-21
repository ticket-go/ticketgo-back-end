from django.contrib.auth import logout, get_user_model
from django.shortcuts import redirect
from apps.users.permissions import AllowCreateOnly
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.api import serializers
from apps.users.models import CustomUser

CustomUser = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "user_id"
    # permission_classes = [AllowCreateOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        if username and CustomUser.objects.filter(username=username).exists():
            return Response(
                {"error": "Este usuário já está em uso por outro usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data.get("email")
        if email and CustomUser.objects.filter(email=email).exists():
            return Response(
                {"error": "Este endereço de e-mail já está em uso por outro usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        return Response(
            {
                "TicketGo": f"O usuário {user.user_id} - {user.username} foi registrado com sucesso."
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        if "password" in serializer.validated_data:
            return Response(
                {"error": "A alteração da senha não é permitida."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_email = serializer.validated_data.get("email")
        if new_email and CustomUser.objects.filter(email=new_email).exists():
            return Response(
                {"error": "Este endereço de e-mail já está em uso por outro usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"O usuário {instance.username} foi deletado com sucesso."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def history(self, request):
        user = request.user
        history = user.history.all()

        history_data = []
        for entry in history:
            if entry.prev_record:
                diff = entry.diff_against(entry.prev_record)
                changes = []
                for change in diff.changes:
                    field = CustomUser._meta.get_field(change.field)
                    verbose_name = field.verbose_name
                    changes.append(
                        {
                            "field": verbose_name,
                            "old_value": change.old,
                            "new_value": change.new,
                        }
                    )
            else:
                changes = "Initial creation"

            history_data.append(
                {
                    "history_id": entry.history_id,
                    "history_date": entry.history_date,
                    "history_change_reason": entry.history_change_reason,
                    "changes": changes,
                }
            )

        return Response(history_data)


class CustomUserChangePasswordViewSet(generics.UpdateAPIView):
    serializer_class = serializers.CustomUserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"detail": "Senha antiga incorreta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
        )


class LoginViewSet(APIView):

    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
                )

            if not user.check_password(password):
                return Response(
                    {"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                access_token = RefreshToken.for_user(user)
            except TokenError as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            user_data = serializers.CustomUserSerializer(user).data

            return Response(
                {
                    "access_token": str(access_token.access_token),
                    "refresh_token": str(access_token),
                    "user": user_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None, responses={200: OpenApiResponse(description="Logout successful")}
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Usuário não autenticado."},
                status=status.HTTP_403_FORBIDDEN,
            )
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
