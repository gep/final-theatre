from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db.models import Sum, Count
from django.views.generic import ListView
from ticket.auth.courieraccessmixin import CourierAccessMixin
from ticket.models import PlayProduction, Ticket

__author__ = 'gep'


class CourierView(CourierAccessMixin, ListView):
    template_name = 'ticket/courier/index.html'
    model = User
    redirect_uri = 'courier'

    @property
    def production(self):
        return PlayProduction.objects.get(pk=self.kwargs['production_id'])

    @property
    def play(self):
        return self.production.play

    @property
    def productions(self):
        return PlayProduction.objects.filter(play=self.production.play)

    def get_redirect_url(self):
        """
        Returns the supplied success URL.
        """
        return reverse(self.redirect_uri, kwargs={'production_id': self.production.id})

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model.objects.filter(
                ticket__is_bought=False,
                ticket__in=Ticket.objects.filter(production=self.production)
            ).distinct().annotate(ticket_count=Count('ticket'), price_sum=Sum('ticket__category__price'))
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)
        # raise Exception(queryset)
        return queryset