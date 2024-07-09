from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.api.views import UserViewSet
from apps.address.api.views import AddressViewSet
from apps.events.api.views import EventsViewSet
from apps.financial.api.views import PaymentsViewSet, PurchasesViewSet
from apps.tickets.api.views import TicketsViewSet
from apps.organizations.api.views import OrganizationViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("events", EventsViewSet)
events_router = routers.NestedSimpleRouter(router, "events", lookup="event")
events_router.register("tickets", TicketsViewSet, basename="event-tickets")

router.register("addresses", AddressViewSet)
router.register("organizations", OrganizationViewSet)
router.register("purchases", PurchasesViewSet)
router.register("payments", PaymentsViewSet)
router.register("users", UserViewSet)

urlpatterns = router.urls + events_router.urls

urlpatterns += [
    path("admin/", admin.site.urls),
    path("api/payments/", include("apps.financial.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/user/", include("apps.users.urls")),
    path("api/", include("apps.tickets.urls"), name="api-tickets"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
]
