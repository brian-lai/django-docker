import re

from google.cloud.exceptions import NotFound
from storages.backends.gcloud import GoogleCloudFile

from core.storage_backends import BioinformaticsCloudStorage, GISTDropboxCloudStorage


STORAGE_BACKENDS = {
    backend.bucket_name: backend()
    for backend in (BioinformaticsCloudStorage, GISTDropboxCloudStorage)
}


# Help identify bucket name prefix
bucket_prefix = r'gs://(?P<bucket_name>[^/]+)/'


def to_relative_path(path):
    '''Converts a gs:// URL to a relative path from the bucket.
    '''
    return re.sub(bucket_prefix, '', path)


def get_bucket_name(path):
    '''Returns the bucket name given a well-formed URL.
    '''
    match = re.match(bucket_prefix, path)
    if match is not None:
        match = match.group('bucket_name')
    return match


def get_storage_backend(bucket_name):
    '''Returns the configured storage backend if available for specified bucket.
    '''
    try:
        storage = STORAGE_BACKENDS[bucket_name]
        return storage
    except IndexError:
        raise RuntimeError('`%s` is not a bucket assoicated with a configured storage backend.')


def get_bucket_from_url(url):
    '''Returns the storage backend, if imported above, by bucket name.
    '''
    bucket_name = get_bucket_name(url)
    return get_storage_backend(bucket_name).bucket


def get_blob_from_url(url):
    '''Returns a blob dynamically from a storage backend given an absolute gs:// URL.
    '''
    bucket = get_bucket_from_url(url)
    return bucket.get_blob(to_relative_path(url))


def get_file_from_url(url):
    '''Returns a `GoogleCloudFile` from `django-storages` to give a file like interface.
    '''
    bucket_name = get_bucket_name(url)
    path = to_relative_path(url)
    storage_backend = get_storage_backend(bucket_name)

    # Check to make sure we found a file
    google_file = GoogleCloudFile(path, 'rb', storage_backend)
    if not google_file.blob:
        raise IOError('File does not exist: %s' % path)

    # Retreive the initial file and rename it
    return google_file


def upload(destination, data):
    '''Creates a new `Blob` in the bucket of choice.

    `destination` is an absolute path `gs://<bucket_name>/<path_to_file>
    and `data` should be either a string or a file handler.
    '''
    bucket = get_bucket_from_url(destination)
    blob = bucket.blob(to_relative_path(destination))

    # Check if the data is a file, read the contents like a file
    if isinstance(data, (str, unicode)) is False:
        data = data.read()

    # Upload the string contents
    blob.upload_from_string(data)


def transfer(source, destination):
    '''Transfers from `source` to `destination`.
    '''
    blob = get_blob_from_url(source)
    if blob is None:
        raise NotFound(u'File not found at source: {}'.format(source))

    # Retrieve destination bucket and perform rename
    bucket = get_bucket_from_url(destination)
    return bucket.rename_blob(blob, to_relative_path(destination))


def idempotent_transfer(source, destination):
    '''Transfers from `source` to `destination`
    Raises NotFound if file doesn't exist at source or destination.
    '''
    try:
        transfer(source, destination)
    except NotFound:
        if get_blob_from_url(destination) is None:
            raise NotFound(u'File not found at source {} or destination {}'.format(source, destination))
