from django.contrib.auth.models import Group
from ticket.auth.courieraccessmixin import CourierAccessMixin

__author__ = 'gep'

from django.views.generic import ListView
from ticket.models import Play


class PlayView(ListView):
    model = Play
    template_name = "ticket/plays.html"