from django.urls import path

from apps.tickets.views import VerifyTicketViewSet

urlpatterns = [
    path(
        "events/<str:event_uuid>/",
        VerifyTicketViewSet.as_view(),
        name="verify_ticket",
    ),
]
