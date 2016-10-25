# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.static import serve
from vanilla.views import RedirectView

from core.admin import site

from .router import urlpatterns as api_urlpatterns


urlpatterns = [
    url(r'^$',
        RedirectView.as_view(permanent=False,
                             url=reverse_lazy('onetime:index')),
        name='index'),

    url(r'^api/v1/', include(api_urlpatterns, namespace='api')),

    # login/logout
    url(r'^login/$', login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'account/logout.html',
                               'next_page': '/'}, name='logout'),

    # admin
    url(r'^admin/', include(site.urls)),

    url(r'^one-time-secret/', include('onetime.urls', namespace='onetime')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL[1:]),
            serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
