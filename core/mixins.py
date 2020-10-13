'''Core app mixins.'''

import csv
from datetime import datetime
import json
import logging

from django import forms
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.forms.utils import ErrorList
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, UpdateView

from core.utils import Echo
from research.utils.general import get_nested_value

logger = logging.getLogger(__name__)


class AtomicTransactionMixin(object):
    '''Ensures DB transactions are rolled back in the event of an error.

    This is particularly useful when a view makes multiple changes to
    the state of the database, and errors can occur during their creation
    or the code surrounding it. Either all changes are committed, or
    nothing.
    '''
    @transaction.atomic
    def dispatch(self, *args, **kwargs):
        return super(AtomicTransactionMixin, self).dispatch(*args, **kwargs)


class CacheMixin(object):
    cache_timeout = 60
    cache_key_prefix = None

    def get_cache_timeout(self):
        return self.cache_timeout

    def get_cache_key_prefix(self):
        return self.cache_key_prefix

    def dispatch(self, *args, **kwargs):
        return cache_page(
            self.get_cache_timeout(),
            key_prefix=self.get_cache_key_prefix()
        )(super(CacheMixin, self).dispatch)(*args, **kwargs)


class SensitivePostParametersMixin(object):
    sensitive_parameters = []

    def dispatch(self, *args, **kwargs):
        return sensitive_post_parameters(
            *self.sensitive_parameters
        )(
            super(SensitivePostParametersMixin, self).dispatch
        )(*args, **kwargs)


class XFrameOptionsExemptMixin(object):
    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(XFrameOptionsExemptMixin, self).dispatch(request, *args, **kwargs)


class LogEntryMixin(object):
    def _log_action(self, action, message='', user=None, instance=None):
            # Exctract the object either by user choice or default
            obj = (instance or getattr(self, 'object', None))
            LogEntry.objects.log_action(
                user_id=(user or self.request.user).id,
                content_type_id=ContentType.objects.get_for_model(obj).id,
                object_id=obj.id,
                object_repr=unicode(obj),
                action_flag=action,
                change_message=message
            )


class LogEntryCreateUpdateMixin(LogEntryMixin):
    def form_valid(self, form):
        ret = super(LogEntryCreateUpdateMixin, self).form_valid(form)

        action = None
        message = ''
        # Determines the type of log entry
        if isinstance(self, CreateView):
            action = ADDITION
        elif isinstance(self, UpdateView):
            action = CHANGE
            # Log the data which changed
            if form.has_changed():
                changed_data = {
                    field: '%s => %s' % (
                        unicode(form.initial.get(field, None)),
                        unicode(getattr(form.cleaned_data.get(field, None), 'id', form.cleaned_data.get(field, None)))
                    ) for field in form.changed_data
                }
                message = json.dumps(changed_data)
        # If there is not request available, we have to return
        if not hasattr(self, 'request'):
            raise NotImplementedError('User was not available for detailed logging.')

        # Only if an action is specified should we log
        if action is not None:
            self._log_action(
                action=action,
                message=message
            )

        return ret


class TemplateViewStatusMixin(object):
    '''Customizes HTTP status code returned by `TemplateView`.
    '''
    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = getattr(self, 'status_code', 200)
        return super(TemplateViewStatusMixin, self).render_to_response(context, **response_kwargs)


class ExportMixin(object):
    """
    Mixin adding exporting to list views.

    It particularly plays nice with django-tables2 views,
    but it should work with any list view.

    Requires either definition of 'export_template_name', definition of 'export_columns' or
    inheritance from django_tables2.SingleTableView.
    """
    def __init__(self, **kwargs):
        super(ExportMixin, self).__init__(**kwargs)
        # set names and accessors
        self.names = []
        self.accessors = []

    export_content_type = 'text/tsv'
    export_content_extension = 'tsv'
    export_filename = 'export'
    export_always = False
    export_columns = None
    export_template_name = None

    def set_names_and_accessors(self):
        # find out if there is a runtime override
        self.export_columns = self.get_export_columns()

        # use column definition if one is present
        if self.export_columns is not None:
            for column in self.export_columns:
                name, accessor = column
                self.names.append(name)
                self.accessors.append(accessor)
        else:
            raise ImproperlyConfigured(
                "ExportMixin requires either definition of 'export_template_name' or definition of 'export_columns'."
            )

    def get_export_columns(self):
        # take the list to make a copy of the export_columns to avoid duplicating columns
        return list(self.export_columns) if self.export_columns else None

    def get_filename(self):
        return '{}_{}'.format(self.export_filename, datetime.today().strftime('%Y-%m-%d'))

    def get_file_content_extension(self):
        return self.export_content_extension

    def get_row(self, obj):
        """
        Returns a list of values obtained using the class accessors. Supports callable accessors.
        """
        row = []
        for accessor in self.accessors:
            if '.' in accessor:
                # If the accessor is provided with a '.', get the nested value from within the object
                value = get_nested_value(obj, accessor.split('.'))
            else:
                value = getattr(obj, accessor, None)

                if callable(value):
                    value = value()

            row.append(value)
        return row

    def stream(self):
        """
        Generator for the data stream in the queryset.

        It will use columns definition if one is present through
        `export_columns` or it will try to piggyback from the table class.
        """
        # calling here to make sure we already have request, needed for is_staff
        self.set_names_and_accessors()

        # yield the header names
        yield self.names

        for obj in self.object_list:
            # yield the row data
            yield self.get_row(obj)

    def render_to_response(self, context, **kwargs):
        """
        Overriding in case we need to render a export stream.
        """
        # if export get variable present, set content type using the class data export content type
        if 'export' in self.request.GET or self.export_always:
            export_response_kwargs = {
                'content_type': self.export_content_type,
            }

            # create the response using the export template if we have one
            if self.export_template_name is not None:
                # load template
                template = loader.get_template(self.export_template_name)

                # create response object
                response = HttpResponse(**export_response_kwargs)

                # write data to the response object using the provided context
                response.write(template.render(context))

            # else try streaming the data using export columns or piggybacking the table view
            else:
                pseudo_buffer = Echo()
                writer = csv.writer(pseudo_buffer, delimiter='\t')

                # Create the StreamingHttpResponse object
                response = StreamingHttpResponse(
                    (writer.writerow(row) for row in self.stream()),
                    **export_response_kwargs
                )

            # set the export filename
            response['Content-Disposition'] = 'attachment; filename=\'%(filename)s.%(extension)s\'' % {
                'filename': self.get_filename(),
                'extension': self.get_file_content_extension()
            }

            # return the exporting response
            return response

        # otherwise return super
        return super(ExportMixin, self).render_to_response(context, **kwargs)


class RelatedTagsMixin(object):
    """Adds a select multiple widget with only related tags.
    """
    def __init__(self, *args, **kwargs):
        super(RelatedTagsMixin, self).__init__(*args, **kwargs)

        # limit related tags choices
        related_tags = self.queryset.exclude(
            tags__isnull=True
        ).order_by(
            "tags__name"
        ).values_list(
            "tags__name", flat=True
        ).distinct()

        # save tags choices
        tags_choices = ((t, t.replace('_', ' ')) for t in related_tags)

        # set tags choices
        self.form.fields["tags"].choices = tags_choices


class StaffMixin(object):
    staff_role = None
    staff_only_fields = None

    def is_staff(self):
        return getattr(self.staff_role, 'check_membership')(self.request.user)

    def get_filterset(self, filterset_class):
        """
        Returns an instance of the filterset to be used in this view.

        Overriding to pop fields that should not be displayed to non-staff users.
        """
        filterset = super(StaffMixin, self).get_filterset(filterset_class)

        if not self.is_staff() and self.staff_only_fields is not None:
            # pop the staff only fields
            for field in self.staff_only_fields:
                filterset.filters.pop(field, None)
                filterset.form.fields.pop(field, None)
        return filterset

    def get_table(self):
        table = super(StaffMixin, self).get_table()

        if not self.is_staff():
            table.exclude = self.staff_only_fields
        return table


class FormUserMixin(object):
    '''Adds the `User` associated with the current request to the form **kwargs.

    Intended to be inherited on view. To function properly, the form must inherit the
    `UserFormMixin`
    '''
    user_kwargs_name = 'user'

    def get_user_kwargs_name(self):
        '''Allows the dynamic configuration of the kwargs name.
        '''
        return self.user_kwargs_name

    def get_form_kwargs(self):
        '''Adds to **kwargs the `User` instance.
        '''
        kwargs = super(FormUserMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserFormMixin(object):
    """Attaches a User passed as a kwarg to a form.

    Intended to be used by forms in conjunction
    with the `FormUserMixin` on the view.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserFormMixin, self).__init__(*args, **kwargs)


class ErrorMessagesMixin(object):
    '''Uses messages framework to provide forms errors after a page redirection. Useful for modal forms.
    '''
    def form_invalid(self, form):
        # Add error messages to messages framework.
        for field, errors in form.errors.iteritems():
            # Check if we need to unpack multiple values
            if not isinstance(errors, ErrorList):
                errors = [errors, ]

            # We don't want to display __all__ in the error message.
            for error in errors:
                if field == "__all__":
                    message_text = error
                else:
                    message_text = "%s: %s" % (field, error)
                messages.error(self.request, message_text)
        return super(ErrorMessagesMixin, self).form_invalid(form)
