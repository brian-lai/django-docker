import csv
import xlrd

from django.core.exceptions import ValidationError


class SpreadsheetUploader(object):
    '''Generic code that can be used to convert an uploaded CSV or Excel file into a dict.

    Any inheriting objects should override validate_data_structure(), and process_uploaded_data().
    '''
    def process_upload(self, in_memory_file, *args, **kwargs):
        '''Main driver function.

        Converts uploaded spreadsheet to dict, and then processes the data.
        '''
        data_dict = self._get_file_as_dict(in_memory_file)
        self.process_uploaded_data(data_dict, **kwargs)

    def _get_file_as_dict(self, in_memory_file):
        '''Return xls, xlsx and csv files as Dicts.
        '''
        file_extension = in_memory_file.name.split(".")[-1]
        data_dict = None

        if file_extension == 'xls' or file_extension == 'xlsx':
            data_dict = SpreadsheetUploader._xls_to_dict(in_memory_file)
        elif file_extension == 'csv':
            data_dict = SpreadsheetUploader._csv_to_dict(in_memory_file)
        else:
            raise ValidationError('Invalid file extension.')

        if self.validate_data_structure(data_dict):
            return data_dict
        else:
            raise ValidationError(('Malformed Data Error.'
                                   ' Please ensure headers are correct,'
                                   ' and all required fields are filled in.'))

    @staticmethod
    def _csv_to_dict(csvpath):
        '''Converts a csv file to a dict.
        '''
        dictreader = csv.DictReader(open(csvpath, 'rU'), dialect='excel')
        data = []
        for row in dictreader:
            data.append(row)
        return data

    @staticmethod
    def _xls_to_dict(in_memory_xls):
        '''Convert .xls file to a dictionary.
        '''
        workbook = xlrd.open_workbook(file_contents=in_memory_xls.read(), on_demand=True)
        worksheet = workbook.sheet_by_index(0)
        first_row = []  # The row where we stock the name of the column
        for col in range(worksheet.ncols):
            first_row.append(worksheet.cell_value(0, col))
        # transform the workbook to a list of dictionnary
        data = []
        for row in range(1, worksheet.nrows):
            elm = {}
            for col in range(worksheet.ncols):
                elm[first_row[col]] = worksheet.cell_value(row, col)
            data.append(elm)
        return data

    def validate_data_structure(self, data_dict):
        '''Returns a Boolean stating whether the data is in proper format before processing.

        Must be overidden in child class.
        '''
        raise NotImplementedError('validate_data_structure() not Implemented in %s' % str(self.__class__))

    def process_uploaded_data(self, data_dict, *args, **kwargs):
        '''After spreadsheet is converted to dict, use data to create new objects.

        Must be overridden in child class.
        '''
        raise NotImplementedError('process_uploaded_data() not Implemented in %s' % str(self.__class__))
