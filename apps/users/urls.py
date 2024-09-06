from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.users.views import (
    LoginViewSet,
    LoginMobileViewSet,
    CustomUserChangePasswordViewSet,
    LogoutViewSet,
    SocialLoginViewSet,
    UserViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

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

urlpatterns += router.urls