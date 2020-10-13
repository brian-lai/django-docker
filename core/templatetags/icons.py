import warnings

from django import template

register = template.Library()


@register.inclusion_tag('core/components/small-action-icon.html', takes_context=True)
def small_action_icon(context, icon, **kwargs):
    return action_icon(context, icon, **kwargs)


@register.inclusion_tag('core/components/large-action-icon.html', takes_context=True)
def large_action_icon(context, icon, **kwargs):
    if kwargs.get('css_id'):
        kwargs['action_css_id'] = kwargs['css_id']
    return action_icon(context, icon, **kwargs)


@register.inclusion_tag('core/components/action-dropdown-item.html', takes_context=True)
def action_dropdown_item(context, icon, **kwargs):
    kwargs['form'] = True
    if kwargs.get('css_id'):
        kwargs['action_css_id'] = kwargs['css_id']
    return action_icon(context, icon, **kwargs)


def action_icon(context, icon, url=None, modal=False, form=False,
                tooltip_message='', action_css_id='', css_classes='',
                confirm_message=None, download=False, highlight=False,
                **kwargs):
    '''Generates HTML for portlet 'action' icons found in the top-right corner.

    The provided parameters allows the buttons appearance to remain the same
    in all instances, but with different levels of element nesting depending
    on if a <form> needs to be included or if content spawns a modal dialog.

    Bootstrap modals are used via data-toggle='modal' and Bootstrap Confirm
    plugin is used for displaying pop-up confirmation actions.

    NOTE: The `form` and `modal` `Booleans` are mutually exclusive, so both
    cannot be set at the same time.

    Attributes:
        url (str): URL the action button should trigger
        is_glyphicon (str): `Boolean` deterministic of icon type being Glyphicons
        icon (str): CSS class to apply for iconography of the button
        form (bool): Should this button trigger a HTML form submission to `url`?
        modal (bool): Should this button open `url` in a modal?
        tooltip_message (str): Hover text to display for action button
        action_css_id (str): Provide a unique CSS id for the button(usually for JS hooks)
        confirm_message (str): Prompt for user when asked to confirm an action
        highlight (bool): Should the icon show a 'pressed' status

    Raises:
        ValueError:
            - Cause: `form` and `modal` are both set, these options are mutually
            exclusive since the `modal` javascript will override the form in
            all cases.
    '''
    if modal and form:
        raise ValueError('Please declare either `form` or `modal` as `True`, but not both.')

    # Deprecation warnings
    if kwargs.get('action_css_id', None) and not kwargs.get('css_id', None):
        warnings.warn(
            'Kwargs `action_css_id` will be deprecated in favor of shorter `css_id`.',
            DeprecationWarning,
            stacklevel=2
        )

    # Parsing context
    if 'glyphicons' in icon:
        icon = 'glyphicons %s' % icon

    local_context = {
        'url': url or context.get('url', ''),
        'icon': icon,
        'form': form,
        'modal': modal,
        'tooltip_message': tooltip_message,
        'confirm_action': bool(confirm_message),
        'css_id': action_css_id,
        'action_css_id': action_css_id,
        'css_classes': css_classes,
        'confirm_message': confirm_message,
        'download': download,
        'highlight': highlight,
        'data_attrs': {}
    }

    # Add modal attribute
    if modal:
        local_context['data_attrs']['data-target'] = '#dynamic-modal'

    # Adds data-attributes automatically
    for key, val in kwargs.iteritems():
        if key.startswith('data_'):
            local_context['data_attrs'][key.replace('_', '-')] = val
    return local_context
