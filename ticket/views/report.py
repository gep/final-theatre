from django.db.models import Sum
from django.views.generic import TemplateView
from registration.models import User
from ticket.auth.courieraccessmixin import CourierAccessMixin
from ticket.models import PlayProduction, SeatCategory

__author__ = 'gep'


class CourierReportView(CourierAccessMixin, TemplateView):
    template_name = 'ticket/courier/report.html'

    @property
    def production(self):
        return PlayProduction.objects.get(pk=self.kwargs['production_id'])

    def get_context_data(self, **kwargs):
        kwargs['category_report'] = self._category_report()
        kwargs['user_report'] = self._user_report()
        return super(CourierReportView, self).get_context_data(**kwargs)

    def _category_report(self):
        report = {'categories': [], 'total_sum': 0}

        for category in SeatCategory.objects.all():
            ticket_sum = category.ticket_set\
                .filter(is_bought=True, production=self.production)\
                .aggregate(category_total_bought_sum=Sum('category__price'))
            ticket_sum = (ticket_sum['category_total_bought_sum'] is not None and [ticket_sum['category_total_bought_sum']] or [0])[0]
            report['total_sum'] += ticket_sum
            report['categories'].append(
                {
                    'category': category,
                    'tickets_left': category.max_seats - category.ticket_set.filter(production=self.production).count(),
                    'tickets_amount': category.ticket_set.filter(production=self.production).count(),
                    'payed_tickets': category.ticket_set.filter(production=self.production, is_bought=True).count(),
                    'tickets_payed_money': ticket_sum
                }
            )
        return report

    def _user_report(self):
        report = {'users': [], 'total_sum': 0}

        for user in User.objects.filter(ticket__in=self.production.ticket_set.filter(is_bought=False)).distinct():
            ticket_sum = user.ticket_set\
                .filter(production=self.production, is_bought=False)\
                .aggregate(total_cost=Sum('category__price'))
            ticket_sum = (ticket_sum['total_cost'] is not None and [ticket_sum['total_cost']] or [0])[0]
            report['total_sum'] += ticket_sum
            report['users'].append({
                'user': user,
                'total_cost': ticket_sum,
                'categories': SeatCategory.objects.filter(ticket__in=user.ticket_set.filter(production=self.production, is_bought=False)).distinct(),
                'tickets_amount': user.ticket_set.filter(production=self.production, is_bought=False).count(),
            })
        return report
