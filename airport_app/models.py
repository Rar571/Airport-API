import pathlib
import uuid

from django.conf import settings
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="routes_source")
    destination = models.ForeignKey(Airport, on_delete=models.DO_NOTHING, related_name="routes_destination")
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"From '{self.source}' to '{self.destination}'"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights_route")
    airplane = models.ForeignKey("Airplane", on_delete=models.DO_NOTHING, related_name="flights_airplane")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField("Crew")

    def __str__(self):
        return f"Flight: [{self.id}] - {self.route} [Departure: {self.departure_time.strftime('%Y-%m-%d %H:%M')}]"


def airplane_image_path(instance: "Airplane", filename: str):
    filename = f"{instance.name}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path("upload_to/airplanes/") / pathlib.Path(filename)


class Airplane(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.DO_NOTHING, related_name="airplanes")
    image = models.ImageField(null=True, upload_to=airplane_image_path)

    def __str__(self):
        return f"{self.name}"

    def capacity(self):
        return self.rows * self.seats_in_row


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING, related_name="tickets_flight")
    order = models.ForeignKey("Order", on_delete=models.CASCADE,
                              null=True, blank=True, related_name="available_tickets")

    class Meta:
        ordering = ("seat",)

    def __str__(self):
        return f"Ticket: [{self.id}] ({self.flight})"

    @staticmethod
    def validate_seat(seat: int, capacity: int, error_to_raise):
        if not (1 <= seat <= capacity):
            raise error_to_raise(
                f"Seat must be in range: 1 - {capacity}"
            )

    def validate(self):
        Ticket.validate_seat(self.seat, self.flight.airplane.capacity(), ValueError)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
