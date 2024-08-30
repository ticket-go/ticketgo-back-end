from django.urls import path, include
from rest_framework import routers
from apps.events.views import EventsViewSet

router = routers.DefaultRouter()
router.register(r'events', EventsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
