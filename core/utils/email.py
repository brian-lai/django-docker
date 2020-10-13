from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

from core.background.utils import enqueue_task
from core.utils.mailchimp import synchronize_mailchimp_digital_ad_list, synchronize_mailchimp_onboarding_list


def _send(emails, subject, plain_text_template_name, plain_text_context,
          html_template_name, html_context, from_email):
    # Define sender and template
    default_from_email = '{admin} <{email}>'.format(
        admin=settings.ADMIN_GROUP,
        email=settings.DEFAULT_FROM_EMAIL
    )
    plain_text_template = get_template(plain_text_template_name).render(plain_text_context)

    kwargs = {}
    # Check if an explicit HTML template or context was passed in
    if html_template_name is not None:
        html_context = html_context or plain_text_context
        kwargs['html_message'] = get_template(html_template_name).render(html_context)

    # Send all emails separately
    for email in emails:
        send_mail(
            subject,
            plain_text_template,
            from_email or default_from_email,
            [email, ],
            **kwargs
        )


def send_email(emails, subject, plain_text_template_name, plain_text_context,
               html_template_name=None, html_context={}, from_email=None):
    '''Wrapper method for sending emails

    Abstracts away implementation and internal/external email clients
    from the user.

    Args:
        emails (list): List of emails which are the recipients
        subject (str): Subject of the email aka title of the message
        plain_text_template_name (str): Path to plain text template
        plain_text_context (dict): Default context for rendering both email templates
        html_template_name (str, optional): Path to html template
        html_context (dict, optional): Secondary context for html template if different
            from the plain text context above
        from_email (str, optional): Sender of the email; Defaults to <ADMIN_GROUP> <DEFAULT_FROM_EMAIL>
    '''
    # Send the email task off to RQ
    enqueue_task(
        None,
        _send,
        emails,
        subject,
        plain_text_template_name,
        plain_text_context,
        html_template_name,
        html_context,
        from_email
    )


def synchronize_mailing_lists():
    '''Abstracts away mailing platform we use, and synchronizes a list of `Users`.

    This function should always be called in the background since it will block for
    a very long time.
    '''
    synchronize_mailchimp_onboarding_list()
    synchronize_mailchimp_digital_ad_list()
