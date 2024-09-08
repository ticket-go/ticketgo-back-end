from django.urls import path
from apps.users.views import (
    LoginViewSet,
    LoginMobileViewSet,
    CustomUserChangePasswordViewSet,
    LogoutViewSet,
    SocialLoginViewSet,
)

urlpatterns = [
    path("login/", LoginViewSet.as_view(), name="login"),
    path("login-mobile/", LoginMobileViewSet.as_view(), name="login-mobile"),
    path("logout/", LogoutViewSet.as_view(), name="logout"),
    path("social-login/<str:provider>/", SocialLoginViewSet.as_view()),
    path(
        "<str:user_id>/change-password/",
        CustomUserChangePasswordViewSet.as_view(),
        name="change-password",
    ),
]
