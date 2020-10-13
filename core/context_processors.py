from django.conf import settings as django_settings


def settings(request):
    '''Settings variables needed in the template.
    '''
    return {
        'COOKIE_DOMAIN': django_settings.CSRF_COOKIE_DOMAIN,
    }
