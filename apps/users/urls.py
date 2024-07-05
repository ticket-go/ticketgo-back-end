from django.urls import path
from apps.users.api.views import (
    LoginViewSet,
    CustomUserViewSet,
    CustomUserChangePasswordViewSet,
    CustomUserChangeEmailViewSet,
    LogoutViewSet,
    SocialLoginViewSet,
)

urlpatterns = [
    path("register/", CustomUserViewSet.as_view(), name="register"),
    path("login/", LoginViewSet.as_view(), name="login"),
    path(
        "change-password/",
        CustomUserChangePasswordViewSet.as_view(),
        name="change password",
    ),
    path("change-email/", CustomUserChangeEmailViewSet.as_view(), name="change e-mail"),
    path("logout/", LogoutViewSet.as_view(), name="logout"),
    path("social-login/<str:provider>/", SocialLoginViewSet.as_view()),
]
