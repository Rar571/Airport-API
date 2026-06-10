from django.contrib import admin

from airport_app.models import (Airport,
                                Route,
                                Flight,
                                Airplane,
                                Crew,
                                AirplaneType,
                                Ticket,
                                Order)


admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Airplane)
admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Ticket)
admin.site.register(Order)
