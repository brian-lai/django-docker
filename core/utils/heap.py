import requests

from django.conf import settings
from django.contrib.auth.models import User


def add_user_properties(user, properties):
    '''Uses Heap Analytics sever-side API to attribute user properties.
    '''
    user_id = user
    if isinstance(user, User):
        user_id = user.id

    # Make the HTTP request
    response = requests.post(
        'https://heapanalytics.com/api/add_user_properties',
        json={
            'app_id': settings.HEAP_ANALYTICS_APP_ID,
            'identity': user_id,
            'properties': properties
        },
        headers={
            'accept': 'application/json',
            'content-type': 'application/json'
        }
    )
    return response.status_code == 200
