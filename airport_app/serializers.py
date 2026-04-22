from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from airport_app.models import Airport, Route, Flight, Airplane, Crew, AirplaneType, Ticket, Order


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airport.objects.all()
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airport.objects.all()
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name",
        queryset= AirplaneType.objects.all()
    )
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField()
    airplane = AirplaneSerializer()
    crew = serializers.StringRelatedField(
        many=True,
    )
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightCreateSerializer(FlightSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    airplane = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airplane.objects.all())
    crew = serializers.PrimaryKeyRelatedField(many=True, queryset=Crew.objects.all())


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")
