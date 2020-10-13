from django.conf import settings
from django.contrib.auth.signals import user_logged_in

from django_hosts import resolvers

from core.utils import heap


def _handle_user_logged_in(sender, user, request, **kwargs):
    # Add the JS for a modal redirect
    redirect_url = request.GET.get('ref', None)
    if redirect_url is not None:
        request.logged_in = True
        request.redirect_to = redirect_url
    else:
        redirect_url = resolvers.reverse('index', host='www')


def user_logged_in_heap_profile(sender, user, **kwargs):
    '''Add Heap property for profile
    '''
    if settings.FEATURE_FLAG_HEAP_ANALYTICS:
        heap.add_user_properties(user, {'profile': unicode(user.get_absolute_url())})

user_logged_in.connect(_handle_user_logged_in, dispatch_uid='core_user_logged_in')
user_logged_in.connect(user_logged_in_heap_profile, dispatch_uid='core_user_logged_in_heap')
