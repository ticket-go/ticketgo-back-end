from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .api_router import urlpatterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular.utils import extend_schema_view, extend_schema


# temporary
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularSwaggerView


# temporary
class PublicSpectacularSwaggerView(SpectacularSwaggerView):
    permission_classes = [AllowAny]
    pass


@extend_schema_view(get=extend_schema(exclude=True))
class CustomSpectacularAPIView(SpectacularAPIView):
    permission_classes = [AllowAny]
    pass


urlpatterns += [
    path("admin/", admin.site.urls),
    path("payments/", include("apps.financial.urls")),
    path("accounts/", include("allauth.urls")),
    path("auth/", include("apps.users.urls")),
    path("check-ticket/", include("apps.tickets.urls"), name="api-tickets"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", CustomSpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        # SpectacularSwaggerView.as_view(url_name="api-schema"), temporary
        PublicSpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
