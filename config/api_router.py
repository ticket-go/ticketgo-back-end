from django.conf import settings

from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from apps.users.views import UserViewSet
from apps.address.views import AddressViewSet
from apps.events.views import EventsViewSet
from apps.tickets.views import TicketsViewSet
from apps.financial.views import CartPaymentsViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("events", EventsViewSet)
events_router = routers.NestedSimpleRouter(router, "events", lookup="event")
events_router.register("tickets", TicketsViewSet, basename="event-tickets")

router.register("users", UserViewSet)
router.register("addresses", AddressViewSet)
router.register("payments", CartPaymentsViewSet)
router.register("tickets", TicketsViewSet)

urlpatterns = router.urls + events_router.urls
