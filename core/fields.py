from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile

from core.genomics import GenomicCoordinate, parse_genomic_coordinate


def parse_genomic_coordinate_validate(genomic_coordinate):
    '''Raises `ValueError` as `ValidationError` for Django.
    '''
    try:
        return parse_genomic_coordinate(genomic_coordinate)
    except ValueError as ex:
        raise ValidationError(ex.message)


def convert_genomic_coordinate(genomic_coordinate):
    '''Transforms `GenomicCoordinate` into database values.
    '''
    if isinstance(genomic_coordinate, (str, unicode)):
        genomic_coordinate = GenomicCoordinate(locus=genomic_coordinate)
    if isinstance(genomic_coordinate, GenomicCoordinate):
        return genomic_coordinate.as_long()
    elif isinstance(genomic_coordinate, long):
        return genomic_coordinate
    raise ValidationError('A `GenomicCoordinate` instance or `long` must be provided for serializing')


class GenomicCoordinateField(models.BigIntegerField):
    '''Wrapper class to serialize/deserialize genomic coordinates.
    '''
    descripton = 'Genomic coordinate with chromosome and position data'

    def __init__(self, *args, **kwargs):
        '''Provides field indexing for quick lookups and comparisons.
        '''
        kwargs['db_index'] = True
        super(GenomicCoordinateField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        '''Popping custom kwargs per documentation for custom fields.
        '''
        name, path, args, kwargs = super(GenomicCoordinateField, self).deconstruct()
        del kwargs['db_index']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        '''Deserialize the data from 64-bit integer with bit shifting
        '''
        if value is None:
            return value

        chromosome, position = parse_genomic_coordinate_validate(value)
        return GenomicCoordinate(chromosome=chromosome, position=position)

    def to_python(self, value):
        '''Deserialize the data from 64-bit integer with bit shifting
        '''
        if isinstance(value, GenomicCoordinate) or value is None:
            return value

        chromosome, position = parse_genomic_coordinate_validate(value)
        return GenomicCoordinate(chromosome=chromosome, position=position)

    def get_prep_value(self, value):
        '''Serlialize the data for the DB as 64-bit integer.
        '''
        return convert_genomic_coordinate(value)

    def value_to_string(self, locus):
        '''How to display the data on a form.
        '''
        return str(locus)


class GoogleStorageFieldFile(FieldFile):
    '''Provides gs:// prefixed URLs for relative pathing.
    '''
    @property
    def gs_url(self):
        return 'gs://%(bucket)s/%(path)s' % {
            'bucket': self.storage.bucket_name,
            'path': self.name
        }

    @property
    def signed_url(self):
        blob = self.storage._get_blob(self.name)
        return blob.generate_signed_url(timedelta(seconds=settings.GS_QUERYSTRING_EXPIRE))

    @property
    def url(self):
        self._require_file()
        return self.signed_url


class GoogleStorageFileField(models.FileField):
    '''Provides default alternative storage backend.
    '''
    attr_class = GoogleStorageFieldFile

    def __init__(self, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 1024)
        super(GoogleStorageFileField, self).__init__(**kwargs)
