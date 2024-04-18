from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # django-allauth
    path("accounts/", include("allauth.urls")),
    #
    path("api/", include("config.api_router")),
    path("users/", include("apps.users.urls")),
    # djangorestframework-simplejwt
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
