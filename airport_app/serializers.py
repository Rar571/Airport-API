from rest_framework import serializers

from airport_app.models import Airport, Route, Flight, Airplane, Crew, AirplaneType, Ticket, Order


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airport.objects.all()
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airport.objects.all()
    )
    available_flights = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance", "available_flights")

    def get_available_flights(self, obj):
        return obj.flights_route.count()


class AirportSerializer(serializers.ModelSerializer):
    routes = serializers.PrimaryKeyRelatedField(
        source="routes_source",
        many=True,
        read_only=True
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "routes")


class CrewSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="__str__",
        read_only=True
    )
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AirplaneType.objects.all()
    )
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type", "capacity")


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "image")


class FlightSerializer(serializers.ModelSerializer):
    departure_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()
    crew = serializers.StringRelatedField(
        many=True,
    )
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightRetrieveSerializer(FlightSerializer):
    route = RouteSerializer()
    airplane = AirplaneSerializer()
    crew = serializers.StringRelatedField(
        many=True
    )


class FlightCreateSerializer(FlightSerializer):
    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all()
    )
    airplane = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airplane.objects.all()
    )
    crew = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Crew.objects.all()
    )


class RouteRetrieveSerializer(RouteSerializer):
    available_flights = FlightSerializer(
        many=True,
        source="flights_route",
        read_only=True
    )


class AirportRetrieveSerializer(serializers.ModelSerializer):
    routes = RouteRetrieveSerializer(
        source="routes_source",
        many=True,
        read_only=True
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "routes")


class AirportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")



class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class TicketSerializer(serializers.ModelSerializer):
    is_sold = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order", "is_sold")

    def validate(self, attrs):
        Ticket.validate_seat(
            attrs["seat"],
            attrs["flight"].airplane.capacity(),
            serializers.ValidationError
        )
        return attrs

    def get_is_sold(self, obj):
        if not obj.order:
            return False
        return True


class TicketListSerializer(TicketSerializer):
    flight = serializers.StringRelatedField()


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = Order
        fields = ("id", "created_at")


class OrderCreateSerializer(serializers.ModelSerializer):
    available_tickets = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ticket.objects.filter(order__isnull=True),
    )
    class Meta:
        model = Order
        fields = ("id", "available_tickets")

    def create(self, validated_data):
        tickets_data = validated_data.pop("available_tickets")
        order = Order.objects.create(**validated_data)
        order.available_tickets.set(tickets_data)
        return order

