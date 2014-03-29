from ticket.auth.courieraccessmixin import CourierAccessMixin

__author__ = 'gep'

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import FormView
from ticket.forms import TicketForm, TicketFormSet
from ticket.models import Ticket, PlayProduction, SeatCategory


class OrderFormView(FormView):
    template_name = 'ticket/order.html'
    success_url = 'order-form'
    form_class = TicketForm
    formset_class = TicketFormSet

    @property
    def is_user_courier(self):
        return self.request.user.groups.filter(name=CourierAccessMixin.group_name).count() != 0

    @property
    def categories(self):
        return SeatCategory.objects.all()

    @property
    def is_past_due(self):
        """
        Need to now if this production is up-to-date
        """
        return self.production.is_past_due

    @property
    def total_price(self):
        total_price = 0
        for ticket in Ticket.objects.filter(user=self.request.user, production=self.production):
            total_price += ticket.category.price
        return total_price

    @property
    def production(self):
        return PlayProduction.objects.get(pk=self.kwargs['production_id'])

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return formset_factory(form_class, extra=0, formset=self.formset_class)(**self.get_form_kwargs())

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial_tickets = []

        for category in self.categories:
            production_tickets = Ticket.objects.filter(production=self.production, category=category)
            for index in range(1, category.max_seats + 1):
                initial_ticket_data = {
                    'number': index,
                    'category': category,
                    'production': self.production,
                    'is_ordered': False,
                    'is_yours': False,
                    'price': category.price,
                    'ticket_id': 0
                }
                for ticket in production_tickets:
                    if ticket.number == index:
                        initial_ticket_data['is_ordered'] = True
                        initial_ticket_data['ticket_id'] = ticket.id
                        initial_ticket_data['is_yours'] = self.request.user.id == ticket.user.id
                        break
                initial_tickets.append(initial_ticket_data)
        return initial_tickets

    def form_valid(self, form):
        if self.request.POST.get('action') == 'cancel':
            Ticket.objects.filter(production=self.production, user=self.request.user).delete()
        else:
            for seat in form:
                if seat.cleaned_data['is_ordered']:
                    if int(seat.cleaned_data['ticket_id']) != 0:
                        continue
                    seat.instance.user = self.request.user
                    seat.save()
                elif int(seat.cleaned_data['ticket_id']) != 0:
                    Ticket.objects.get(pk=int(seat.cleaned_data['ticket_id']), user=self.request.user).delete()
        return super(OrderFormView, self).form_valid(form)

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        return reverse(self.success_url, kwargs={'production_id': self.production.id})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(generic.FormView, self).dispatch(request, *args, **kwargs)
