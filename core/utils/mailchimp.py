import logging

from django.conf import settings
from django.contrib.auth.models import User

from mailchimp3 import MailChimp
from mailchimp3.helpers import get_subscriber_hash
from requests import HTTPError

from core.roles import WebsiteUser
from marketing.models import DigitalLead

# Instantiate logger
logger = logging.getLogger('clock')

# Macro for text statuses
SUBSCRIBED = 'subscribed'
DATE_FORMAT = '%m/%d/%Y'


def get_mailchimp_client():
    '''Returns an active Mailchimp client based on settings credentials.
    '''
    return MailChimp(
        settings.MAILCHIMP_USERNAME,
        settings.MAILCHIMP_SECRET_KEY,
        timeout=10.0
    )


def synchronize_mailchimp_email(client, list_id, email, merge_fields, email_type='Email'):
    '''Handles common exceptions thrown by Mailchimp when synchronizing.
    '''
    try:
        # Create or update subscriber
        client.lists.members.create_or_update(
            list_id=list_id,
            subscriber_hash=get_subscriber_hash(email),
            data={
                'email_address': email,
                'status': SUBSCRIBED,
                'status_if_new': SUBSCRIBED,
                'merge_fields': merge_fields
            }
        )
    except HTTPError as ex:
        # Handle Mailchimp complaining about potentially faulty data, don't synchronize
        if ex.response.status_code == 400 and 'fake' in ex.response.content:
            logger.warning(
                'Unable to synchronize `%s %s`, they are suspected to have a fake email' % (
                    email_type, email
                )
            )
        else:
            logger.warning('Unable to synchronize `%s %s`, an unknown error occured' % (email_type, email))
    except ValueError:
        # Someone didn't give a valid email
        logger.warning('Unable to synchronize `%s %s`, invalid email' % (email_type, email))


def synchronize_mailchimp_onboarding_list():
    '''Synchronizes our current set of `Users` in GIST against Mailchimp.

    Additionally synchronizes the following attributes (if applicable):
        * First Name
        * Email
        * Signup Date
        * Purchase Date
        * Report Release Date
    '''
    client = get_mailchimp_client()
    users = User.objects.filter(
        groups__id=WebsiteUser.get_group().id
    ).exclude(email='')
    for user in users:
        # Define extra data to send to Mailchimp
        merge_fields = {
            'FNAME': user.first_name,
            'LNAME': user.last_name,
            'SDATE': user.date_joined.strftime(DATE_FORMAT)
        }

        # Attempt to find purchased `Screens`
        family = user.families_organized.first()
        if family is not None:
            screen = family.screens.first()
            if screen is not None:
                merge_fields['PDATE'] = screen.get_statistics().date_created.strftime(DATE_FORMAT)
                if screen.patient_release is not None:
                    merge_fields['RDATE'] = screen.patient_release.date_signed.strftime(DATE_FORMAT)

        # Synchronize the `User`
        synchronize_mailchimp_email(
            client,
            settings.MAILCHIMP_ONBOARDING_LIST_ID,
            user.email,
            merge_fields,
            email_type='User'
        )


def synchronize_mailchimp_digital_ad_list():
    '''Synchronizes all emails which have downloaded our brochure against Mailchimp.

    Additionally synchronizes the following attributes:
        * First Name
        * Email
    '''
    client = get_mailchimp_client()
    leads = DigitalLead.objects.exclude(
        email__in=User.objects.values_list('email', flat=True)
    )
    for lead in leads:
        # Define extra data to send to Mailchimp
        merge_fields = {
            'FNAME': lead.name
        }

        # Synchronize the `DigitalLead`
        synchronize_mailchimp_email(
            client,
            settings.MAILCHIMP_DIGITAL_AD_LIST_ID,
            lead.email,
            merge_fields,
            email_type='DigitalLead'
        )
