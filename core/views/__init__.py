from django.contrib import messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, TemplateView
from django.views.generic.list import ListView

from core.mixins import LogEntryMixin, TemplateViewStatusMixin


class ErrorView(TemplateView):
    '''Allows all error handlers to be called from any status.
    '''
    def dispatch(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class PermissionErrorView(TemplateViewStatusMixin, ErrorView):
    status_code = 403
    template_name = 'core/errors/403.html'


class PageNotFoundErrorView(TemplateViewStatusMixin, ErrorView):
    status_code = 404
    template_name = 'core/errors/404.html'


class ServerErrorView(TemplateViewStatusMixin, ErrorView):
    status_code = 500
    template_name = 'core/errors/500.html'


class ActionView(LogEntryMixin, UpdateView):
    fields = ()
    logentry_message = None
    template_name = ''

    def dispatch(self, *args, **kwargs):
        '''Dynamically sets fields depending if a `form_class` is present.
        '''
        if getattr(self, 'form_class', None) is not None:
            setattr(self, 'fields', None)
        return super(ActionView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        ret = super(ActionView, self).form_valid(form)

        # Add the LogEntry
        message = self.get_logentry_message()
        if message is not None:
            self._log_action(
                action=CHANGE,
                message=message
            )

        return ret

    def form_invalid(self, form):
        # Call super as a formality
        super(ActionView, self).form_invalid(form)

        # Add all of the errors to the view
        for key, errors in form.errors.iteritems():
            for error in errors:
                messages.error(self.request, error)

        return HttpResponseRedirect(self.get_success_url())

    def get_logentry_message(self):
        return self.logentry_message


class ObjectHistoryView(ListView):
    model = LogEntry
    template_name = 'core/components/object-history.html'

    def get_queryset(self):
        return super(ObjectHistoryView, self).get_queryset().filter(
            content_type=ContentType.objects.get(id=self.kwargs['content_type']),
            object_id=self.kwargs['object_id']
        ).order_by('action_time')


class ScannerModalView(TemplateView):
    template_name = 'core/modals/scanner.html'
