from django.views.generic import TemplateView
from ticket.models import Play

__author__ = 'gep'


class PlayInfoView(TemplateView):
    template_name = 'ticket/playinfo.html'

    def play(self):
        return Play.objects.get(pk=self.kwargs['play_id'])
