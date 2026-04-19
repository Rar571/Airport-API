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
        return f"From '{self.source}' to '{self.destination}'."


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey("Airplane", on_delete=models.DO_NOTHING, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField("Crew")


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE, related_name="airplanes")

    def __str__(self):
        return f"{self.name}, type: {self.airplane_type}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.DO_NOTHING, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
