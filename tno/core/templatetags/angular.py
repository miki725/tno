# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django import template
from django.conf import settings
from django.template import loader
from django.utils.safestring import mark_safe
from django_auxilium.utils.html import simple_minify


register = template.Library()

ANGULAR_TEMPLATE = loader.get_template_from_string(
    '{% include angular_template_name %}')
ANGULAR_SCRIPT_TEMPLATE = loader.get_template_from_string("""
<script type="text/ng-template" id="{{ angular_name }}">{{ template }}</script>
""")


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
