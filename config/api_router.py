from rest_framework import routers

from apps.address.api.views import AddressViewSet
from apps.events.api.views import EventsViewSet

router = routers.SimpleRouter()
router.register("events", EventsViewSet)
router.register("addresses", AddressViewSet)
urlpatterns = router.urls
