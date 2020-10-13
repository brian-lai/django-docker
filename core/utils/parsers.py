import csv
from dateutil import parser as date_parser

import xlrd
from django.core.exceptions import ValidationError


class SpreadsheetParser(object):
    '''Parser for delimited or Excel files, which provides a file-like interface.

    You need to implement the `clean_record()` method to provide schema validation of your
    columns and rows while parsing.
    '''
    EXCEL_FILE_EXTENSIONS = ('xls', 'xlsx')
    DELIMITED_FILE_EXTENSIONS = ('csv', 'tsv')
    DELIMITER_LOOKUP = {
        'tsv': '\t'
    }

    # Arrays for primitive parsing
    booleans = integers = floats = dates = ()

    def __init__(self, input_file, file_type=None):
        '''Takes in the users file and validates the contents.
        '''
        self.file = input_file

        self.headers = []

        self.file_type = self.get_file_type() if file_type is None else file_type

        # Create the iterable for later
        self.generator = self.build_generator()

    def __iter__(self):
        '''Provides iteration over the rows of the file.
        '''
        return self.generator

    def get_file_type(self):
        '''What is the extension of the file provided.
        '''
        return self.file.name.split('.')[-1]

    def build_generator(self):
        '''Returns an iterable-generator for the file.
        '''
        parser = None
        if self.file_type in self.EXCEL_FILE_EXTENSIONS:
            parser = self.excel_parser
        elif self.file_type in self.DELIMITED_FILE_EXTENSIONS:
            parser = self.delimited_parser

        # If we didn't find a parser, complain about the file type we were given
        if parser is None:
            raise ValidationError('Invalid file extension `%s` provided' % self.file_type)

        # Invoke the parser to get results
        return parser()

    def delimited_parser(self):
        '''Parses delimited file with a given delimiter.
        '''
        delimiter = self.DELIMITER_LOOKUP.get(self.file_type, ',')
        reader = csv.DictReader(self.file, delimiter=delimiter)
        for record in reader:
            yield self.clean_record(record)

    def excel_parser(self):
        '''Parses Excel file into rows mimicing `csv.DictReader`.
        '''
        workbook = xlrd.open_workbook(file_contents=self.file.read(), on_demand=True)
        worksheet = workbook.sheet_by_index(0)

        # Extract the headers from the sheet
        for col in range(worksheet.ncols):
            self.headers.append(worksheet.cell_value(0, col))

        # Validate the individual rows now
        for row in range(1, worksheet.nrows):
            record = {}
            for column in range(worksheet.ncols):
                cell = worksheet.cell(row, column)
                value = cell.value
                if cell.ctype == xlrd.XL_CELL_NUMBER:
                    value = int(cell.value)
                record[self.headers[column]] = str(value)

            # Validate and yield the record
            yield self.clean_record(record)

    def clean_record(self, record):
        '''Raises a `ValidationError` if the record doesn't match the expected format.

        Natively parses primitive types from class defined arrays.
        '''
        try:
            # Booleans
            for field in self.booleans:
                value = record[field].title()
                if value == 'True':
                    record[field] = True
                elif value == 'False':
                    record[field] = False
                else:
                    record[field] = None

            # Integers
            for field in self.integers:
                try:
                    record[field] = int(record[field])
                except ValueError:
                    record[field] = None

            # Floats
            for field in self.floats:
                try:
                    record[field] = float(record[field])
                except ValueError:
                    record[field] = None

            # Datetimes
            for field in self.dates:
                record[field] = date_parser.parse(record[field])
        except (TypeError, ValueError):
            raise ValidationError('Unable to parse `%s` for field `%s`' % (record[field], field))

        return record
