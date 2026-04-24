from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from airport_app.models import Airport, Route, Flight, Airplane, Crew, AirplaneType, Ticket, Order
from airport_app.permissions import IsAdminAllORIsAuthenticatedOReadOnly
from airport_app.serializers import AirportSerializer, RouteSerializer, FlightSerializer, CrewSerializer, AirplaneTypeSerializer, TicketSerializer, OrderSerializer, AirplaneSerializer, FlightCreateSerializer, AirportRetrieveSerializer, FlightRetrieveSerializer, RouteRetrieveSerializer, TicketListSerializer, OrderCreateSerializer, AirportCreateSerializer, AirplaneImageSerializer, TicketRetrieveSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)

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
            return (self.queryset.
                    filter(routes_source__id__in=route_id)
                    .prefetch_related("routes_source"))
        if self.action in ("list", "retrieve"):
            return self.queryset.prefetch_related("routes_source")
        return self.queryset
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='route',
                description='Filter by route id',
                type={"type": "array", "items": {"type": "number"}})])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return (self.queryset
                    .select_related("source", "destination")
                    .prefetch_related("flights_route"))
        return self.queryset


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightRetrieveSerializer
        elif self.action in ("create", "put", "patch"):
            return FlightCreateSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.all()
        airplane = self.request.query_params.get("airplane")
        route_source = self.request.query_params.get("route_source")
        route_destination = self.request.query_params.get("route_destination")

        if airplane:
            return queryset.filter(
                airplane__name__icontains=airplane
            )
        if route_source:
            return queryset.filter(
                route__source__name__icontains=route_source
            )
        if route_destination:
            return queryset.filter(route__destination__name__icontains=route_destination)
        return (queryset.
                select_related("route", "airplane",
                               "route__source", "route__destination",
                               "airplane__airplane_type").
                                prefetch_related("crew"))

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='airplane',
                description='Filter by airplane name',
                type={"type": "array", "items": {"type": "string"}}),
            OpenApiParameter(
                name='route source',
                description='Filter by route source',
                type={"type": "array", "items": {"type": "string"}}),
            OpenApiParameter(
                name='route destination',
                description='Filter by route destination',
                type={"type": "array", "items": {"type": "string"}})])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return AirplaneSerializer

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload_image"
    )
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)

    def get_serializer_class(self):
        if self.action in "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketRetrieveSerializer
        return TicketSerializer

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return self.queryset.select_related("flight", "order")
        return self.queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminAllORIsAuthenticatedOReadOnly,)

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        return (self.queryset
                .filter(user=self.request.user)
                .prefetch_related("available_tickets"))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
