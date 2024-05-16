from django.urls import path
from apps.users.api.views import (
    CustomUserReadListViewSet,
    LoginViewSet,
    CustomUserViewSet,
    CustomUserUpdateViewSet,
    CustomUserChangePasswordViewSet,
    CustomUserChangeEmailViewSet,
    LogoutViewSet,
    SocialLoginViewSet,
)

urlpatterns = [
    path("register/", CustomUserViewSet.as_view(), name="register"),
    path("login/", LoginViewSet.as_view(), name="login"),
    path("update/", CustomUserUpdateViewSet.as_view(), name="user update"),
    path(
        "change-password/",
        CustomUserChangePasswordViewSet.as_view(),
        name="change password",
    ),
    path("change-email/", CustomUserChangeEmailViewSet.as_view(), name="change e-mail"),
    path("logout/", LogoutViewSet.as_view(), name="logout"),
    path("social-login/<str:provider>/", SocialLoginViewSet.as_view()),
    path("list/", CustomUserReadListViewSet.as_view()),
]
