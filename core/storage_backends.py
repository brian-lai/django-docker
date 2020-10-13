'''Backend Storage objects for the multiple Google Storage Projects we work with.
'''
import json

from django.conf import settings
from google.oauth2.service_account import Credentials
from storages.backends.gcloud import GoogleCloudStorage


def get_google_credentials(credentials):
    '''Fetches service account credentials from a JSON string.
    '''
    return Credentials.from_service_account_info(json.loads(credentials))


class BioinformaticsCloudStorage(GoogleCloudStorage):
    '''Storage backend for genepeeks-bioinformatics project.
    '''
    bucket_name = settings.GS_BIOINFORMATICS_BUCKET_NAME
    project_id = settings.GS_BIOINFORMATICS_PROJECT_ID
    credentials = get_google_credentials(settings.GS_BIOINFORMATICS_CREDENTIALS)


class GISTDropboxCloudStorage(GoogleCloudStorage):
    '''Storage backend for genepeeks-gist project.
    '''
    bucket_name = settings.GS_GENEPEEKS_GIST_BUCKET_NAME
    project_id = settings.GS_GENEPEEKS_GIST_PROJECT_ID
    credentials = get_google_credentials(settings.GS_GENEPEEKS_GIST_CREDENTIALS)
