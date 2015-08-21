# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django import template
from django_auxilium.utils.html import simple_minify
from django.conf import settings
from django.template import engines
from django.utils.safestring import mark_safe


register = template.Library()
django_engine = engines['django']

ANGULAR_TEMPLATE = django_engine.from_string(
    '{% include angular_template_name %}'
)
ANGULAR_SCRIPT_TEMPLATE = django_engine.from_string(
    '<script type="text/ng-template" id="{{ angular_name }}">{{ template }}</script>'
)


@register.simple_tag(takes_context=True)
def angular_template(context, template_name, angular_name):
    context.update({
        'angular_template_name': template_name,
    })
    content = ANGULAR_TEMPLATE.render(context)
    if not settings.DEBUG:
        content = mark_safe(simple_minify(content))
    context = template.Context({
        'template': content,
        'angular_name': angular_name,
    })
    return ANGULAR_SCRIPT_TEMPLATE.render(context)
