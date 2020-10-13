from django import template

register = template.Library()


@register.inclusion_tag('core/tags/sortable_header.html', takes_context=True)
def sortable_header(context, title, field, *args, **kwargs):
    context.update({'title': title, 'field': field, 'direction': None})

    sort = context['request'].GET.get('sort')

    if field == sort:
        context['field'] = '-' + field
        context['direction'] = 'up'
    elif '-' + field == sort:
        context['field'] = ''
        context['direction'] = 'down'

    return context
