from django.urls import path, include
from rest_framework import routers
from address.api.views import AddressViewSet

router = routers.DefaultRouter()
router.register(r'address', AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]