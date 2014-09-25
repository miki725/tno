# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from vanilla.views import TemplateView


class OneTimeSecretView(TemplateView):
    template_name = 'onetime/index.html'
