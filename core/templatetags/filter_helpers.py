from django import template

register = template.Library()


@register.filter
def form(obj):
    return getattr(obj, 'form')
