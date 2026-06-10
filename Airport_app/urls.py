from django.urls import path, include

from rest_framework import routers

from airport_app.views import (AirportViewSet,
                               RouteViewSet,
                               FlightViewSet,
                               AirplaneViewSet,
                               OrderViewSet, TicketViewSet, AirplaneTypeViewSet, CrewViewSet)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("tickets", TicketViewSet)
router.register("orders", OrderViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("crews", CrewViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "airport_app"

