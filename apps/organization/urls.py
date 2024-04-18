from django.urls import path, include
from rest_framework import routers
from apps.organization.api.views import OrganizationViewSet

router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
