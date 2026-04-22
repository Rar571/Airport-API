from django.shortcuts import render

from rest_framework import viewsets

from airport_app.models import Airport, Route, Flight, Airplane, Crew, AirplaneType, Ticket, Order
from airport_app.serializers import AirportSerializer, RouteSerializer, FlightSerializer, CrewSerializer, AirplaneTypeSerializer, TicketSerializer, OrderSerializer, AirplaneSerializer, FlightCreateSerializer, AirportRetrieveSerializer, FlightRetrieveSerializer, RouteRetrieveSerializer, TicketListSerializer, OrderCreateSerializer, AirportCreateSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirportRetrieveSerializer
        elif self.action == "create":
            return AirportCreateSerializer
        return AirportSerializer

    def _params_to_int(self, query_str: str) -> list:
        return [int(i) for i in query_str.split(",")]

    def get_queryset(self):
        route = self.request.query_params.get("route")
        if route:
            route_id = self._params_to_int(route)
            return self.queryset.filter(routes_source__id__in=route_id)
        return self.queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightRetrieveSerializer
        elif self.action in ("create", "put", "patch"):
            return FlightCreateSerializer
        return FlightSerializer

    def get_queryset(self):
        airplane = self.request.query_params.get("airplane")
        route_source = self.request.query_params.get("route_source")
        route_destination = self.request.query_params.get("route_destination")

        if airplane:
            return self.queryset.filter(
                airplane__name__icontains=airplane
            )
        if route_source:
            return self.queryset.filter(
                route__source__name__icontains=route_source
            )
        if route_destination:
            return self.queryset.filter(route__destination__name__icontains=route_destination)

        return self.queryset


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TicketListSerializer
        return TicketSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
