from django.contrib.auth.models import User
from ticket.auth.courieraccessmixin import CourierAccessMixin
from ticket.forms import CourierTicketFormSet
from ticket.models import Ticket
from ticket.views.orderform import OrderFormView

__author__ = 'gep'


class CourierFormView(CourierAccessMixin, OrderFormView):
    template_name = 'ticket/courier/form.html'
    formset_class = CourierTicketFormSet
    success_url = 'courier'

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
                    'id': 0,
                    'ticket_id': 0,
                    'user_name': '',
                    'user_id': 0,
                    'is_bought': False
                }
                for ticket in production_tickets:
                    if ticket.number == index:
                        initial_ticket_data['is_ordered'] = True
                        initial_ticket_data['ticket_id'] = ticket.id
                        initial_ticket_data['is_bought'] = ticket.is_bought
                        initial_ticket_data['user_id'] = ticket.user_id
                        initial_ticket_data['user_name'] = ticket.user.username
                        initial_ticket_data['is_yours'] = self.request.user.id == ticket.user.id
                        break
                initial_tickets.append(initial_ticket_data)
        return initial_tickets

    def form_valid(self, form):
        if self.request.POST.get('cancel_order') is not None:
            Ticket.objects.filter(production=self.production, user=User.objects.get(pk=int(self.request.POST.get('cancel_order')))).delete()
        elif self.request.POST.get('pay_order') is not None:
            order_user_id = int(self.request.POST.get('pay_order'))
            for seat in form:
                if seat.cleaned_data['is_ordered']:
                    if seat.cleaned_data['ticket_id'] != 0 \
                            and seat.cleaned_data['user_id'] == order_user_id:
                        seat.instance = Ticket.objects.get(pk=seat.cleaned_data['ticket_id'])
                        seat.instance.is_bought = True
                        seat.save()
                elif int(seat.cleaned_data['ticket_id']) != 0:
                    Ticket.objects.get(pk=int(seat.cleaned_data['ticket_id']), user=User.objects.get(pk=order_user_id)).delete()
        return super(OrderFormView, self).form_valid(form)