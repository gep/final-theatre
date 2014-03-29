from django.forms.formsets import BaseFormSet
from ticket.models import Ticket

__author__ = 'Andrey Semikov'
from django import forms


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['production', 'category', 'number', 'id']


class TicketFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(TicketFormSet, self).add_fields(form, index)
        form.fields["is_ordered"] = forms.BooleanField(required=False)
        form.fields["is_yours"] = forms.BooleanField(required=False)
        form.fields["ticket_id"] = forms.IntegerField(required=False)
        form.fields["price"] = forms.IntegerField(required=True)


class CourierTicketFormSet(TicketFormSet):
    def add_fields(self, form, index):
        super(CourierTicketFormSet, self).add_fields(form, index)
        form.fields["user_name"] = forms.CharField(required=False)
        form.fields["user_id"] = forms.IntegerField(required=False)
        form.fields["is_bought"] = forms.BooleanField(required=False)

