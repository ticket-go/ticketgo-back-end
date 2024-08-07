from django.urls import path
from apps.users.api.views import (
    LoginViewSet,
    CustomUserChangePasswordViewSet,
    LogoutViewSet,
    SocialLoginViewSet,
)

urlpatterns = [
    path("login/", LoginViewSet.as_view(), name="login"),
    path("logout/", LogoutViewSet.as_view(), name="logout"),
    path("social-login/<str:provider>/", SocialLoginViewSet.as_view()),
    path(
        "<str:user_id>/change-password/",
        CustomUserChangePasswordViewSet.as_view(),
        name="change-password",
    ),
]
