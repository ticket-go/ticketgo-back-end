from rest_framework import routers

from apps.address.api.views import AddressViewSet
from apps.events.api.views import EventsViewSet
from apps.tickets.api.views import TicketsViewSet

router = routers.SimpleRouter()
router.register("events", EventsViewSet)
router.register("addresses", AddressViewSet)
router.register("tickets", TicketsViewSet)
urlpatterns = router.urls
