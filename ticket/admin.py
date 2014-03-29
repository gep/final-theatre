from django.contrib import admin

from django.contrib import admin
from ticket.models import Play, PlayProduction, SeatCategory, Ticket

admin.site.register(Play)
admin.site.register(PlayProduction)

admin.site.register(SeatCategory)
admin.site.register(Ticket)
