from django.urls import path

from apps.tickets.api.views import VerifyTicketViewSet

urlpatterns = [
    path(
        "events/<str:event_uuid>/tickets/<str:ticket_uuid>/verify/",
        VerifyTicketViewSet.as_view(),
        name="verify_ticket",
    ),
]
