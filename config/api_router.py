from rest_framework import routers

from apps.address.api.views import AddressViewSet
from apps.events.api.views import EventsViewSet
from apps.financial.api.views import PurchasesViewSet
from apps.tickets.api.views import TicketsViewSet
from apps.organizations.api.views import OrganizationViewSet

router = routers.SimpleRouter()

router.register("events", EventsViewSet)
router.register("addresses", AddressViewSet)
router.register("tickets", TicketsViewSet)
router.register("organizations", OrganizationViewSet)
router.register("purchases", PurchasesViewSet)

urlpatterns = router.urls
