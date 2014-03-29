from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

__author__ = 'gep'

LOGIN_URL = '/accounts/login'


class CourierAccessMixin(object):
    group_name = 'courier'

    @property
    def user(self):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=CourierAccessMixin.group_name).count() != 0:
            messages.error(
            request,
            'You do not have the permission required to perform the '
            'requested operation.')
            return redirect(LOGIN_URL, next=self.get_redirect_url())
        return super(CourierAccessMixin, self).dispatch(request, *args, **kwargs)
