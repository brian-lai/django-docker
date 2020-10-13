import sys
import traceback
from django.core import mail
from django.views.debug import ExceptionReporter


def send_exception_email(request, exception, subject=None, exc_info=None):
    '''Adapted from: http://stackoverflow.com/questions/29392281/manually-trigger-django-email-error-report
    '''

    # Allow passing of exc_info
    if exc_info is None:
        exc_info = sys.exc_info()
    reporter = ExceptionReporter(request, is_email=True, *exc_info)

    # Should we auto-gen a subject
    if subject is None:
        subject = exception.message.replace('\n', '\\n').replace('\r', '\\r')[:989]

    # Compile the body of the email
    message = '%s\n\n%s' % (
        '\n'.join(traceback.format_exception(*exc_info)),
        reporter.filter.get_post_parameters(request)
    )
    mail.mail_admins(
        subject, message, fail_silently=True,
        html_message=reporter.get_traceback_html()
    )


class CorruptedDataError(RuntimeError):
    '''Thrown when data does not exist on a database object when it should.
    '''
    pass

    def __init__(self, *args, **kwargs):
        '''Pulls out additional information for later debugging.
        '''
        self.payload = kwargs.pop('payload', {})
        super(CorruptedDataError, self).__init__(*args, **kwargs)

    def send(self, request):
        send_exception_email(request, self)


class FatalDataError(CorruptedDataError):
    '''Irrecoverable data error means the task requiring the information cannot complete, even in partial.

    This is a complete abort of process.
    '''
    pass


class RecoverableDataError(CorruptedDataError):
    '''The process is still able to complete major functions of its work, with only small differences from complete success.

    Data can be fixed manually in most cases here by providing
    small information to the engineering team.
    '''
    pass
