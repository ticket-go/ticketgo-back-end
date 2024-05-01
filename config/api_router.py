from django.conf import settings

from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from apps.address.api.views import AddressViewSet
from apps.events.api.views import EventsViewSet
from apps.financial.api.views import PurchasesViewSet
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

urlpatterns = router.urls + events_router.urls
