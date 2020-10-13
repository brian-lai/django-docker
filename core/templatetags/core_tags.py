from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    """Get a value from settings anywhere on the template"""
    return getattr(settings, name, "")
