from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import RedirectView
from ticket.views.courier import CourierView
from ticket.views.courierform import CourierFormView
from ticket.views.orderform import OrderFormView
from ticket.views.play import PlayView
from ticket.views.report import CourierReportView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'final.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/plays/list/')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='registration-login'),
    url(r'^users/', RedirectView.as_view(url='/')),


    url(r'^admin/', include(admin.site.urls)),

    url(r'^plays/list/$', PlayView.as_view(), name='play-list'),
    url(r'^plays/order/(?P<production_id>\d+)$', OrderFormView.as_view(), name='order-form'),

    url(r'^plays/courier/(?P<production_id>\d+)$', CourierView.as_view(), name='courier'),
    url(r'^plays/courier/update/(?P<production_id>\d+)$', CourierFormView.as_view(), name='courier-form'),
    url(r'^plays/courier/report/(?P<production_id>\d+)$', CourierReportView.as_view(), name='courier-report'),


)
