from django import template
from django.contrib.contenttypes.models import ContentType
from django.db import models

register = template.Library()


@register.filter
def content_type(obj):
    if isinstance(obj, models.Model) is False:
        return False
    return ContentType.objects.get_for_model(obj)


@register.filter
def class_name(obj):
    return unicode(obj.__class__.__name__)


@register.filter
def timedelta(value):
    if value:
        total_seconds = value.seconds + value.days * 24 * 3600
        hours = total_seconds // 3600
        minutes = total_seconds % 3600 // 60
        seconds = total_seconds % 3600 % 60

        return '{hours}h {minutes}m {seconds}s'.format(
            hours=str(hours).zfill(2),
            minutes=str(minutes).zfill(2),
            seconds=str(seconds).zfill(2)
        )


@register.filter
def order_by(queryset, order_by):
    try:
        queryset = queryset.order_by(order_by)
    except AttributeError:
        pass
    return queryset
