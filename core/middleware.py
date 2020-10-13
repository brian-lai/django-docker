from django.utils import timezone


class TimezoneMiddleware(object):
    '''Looks for cookie 'utc_offset' to determine timezone.
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Parse the timezone from the cookie
        tz_offset = -(float(request.COOKIES.get('utc_offset', 0)) * 60)
        if tz_offset:
            timezone.activate(timezone.get_fixed_timezone(tz_offset))
        else:
            timezone.deactivate()

        return self.get_response(request)
