'''
HTML generation for primitive types.
'''
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def boolean(boolean, true_title='True', false_title='False', none_title='None', **kwargs):
    none_glyph = kwargs.get('none_glyph', '')
    if none_glyph == '':
        none_glyph = 'glyphicons glyphicons-question-sign font-grey-cascade'

    true_glyph = kwargs.get('true_glyph', '')
    if true_glyph == '':
        true_glyph = 'glyphicons glyphicons-ok-circle font-green-jungle'

    false_glyph = kwargs.get('false_glyph', '')
    if false_glyph == '':
        false_glyph = 'glyphicons glyphicons-remove-circle font-red'

    html_params = {'glyph': none_glyph, 'title': none_title}
    if boolean is True:
        html_params = {'glyph': true_glyph, 'title': true_title}
    elif boolean is False or (boolean is None and kwargs.get('NoneIsFalse', False)):
        html_params = {'glyph': false_glyph, 'title': false_title}

    return mark_safe('<span class=\'%(glyph)s\' title=\'%(title)s\'></span>' % html_params)
