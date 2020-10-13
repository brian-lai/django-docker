"""
Scanner works with the barcode scanner in order to identify items in the system.
"""
import re


class Scanner:
    """
    Basic interface for retrieving barcode assoicated information.
    """
    # Regular expressions defining the type of barcode we may see
    _barcodes = {
        'Specimen': [
            r'[0-9]{14}',
        ],
        'USPS': [
            r'9[0-9]{21}',
            r'82[0-9]{8}',
            r'7[0-9]{19}',
            r'E[a-zA-Z][0-9]{9}US',
            r'CP[0-9]{9}US',
            r'14[0-9]{18}',
            r'RA[0-9]{9}US',
            r'23[0-9]{18}',
            r'03[0-9]{18}',
        ],
        'UPS': [
            r'1[zZ][0-9A-Z]{16}',
            r'[0-9]{9}([0-9]{3})?',
            r'T[0-9A-Z]{11}',
        ],
        'FedEx': [
            r'[0-9]{12}([0-9]{3})?',
        ],
    }

    # Compile the expressions for easier matching performance
    barcodes = {}
    for key, val in _barcodes.iteritems():
        barcodes[key] = []
        for code in val:
            barcodes[key].append(re.compile(code))

    _shortest_code = 9
    _longest_code = 22

    @staticmethod
    def ordinal_clean(barcode):
        expr = re.compile(r'(?P<barcode>[a-zA-Z0-9]+)')
        match = expr.match(barcode)
        if match is not None:
            return match.group('barcode').decode('unicode_escape').encode('ascii', 'ignore')
        return barcode

    @staticmethod
    def postal_clean(barcode):
        expr = re.compile(r'(420[0-9]{5})?(?P<barcode>[a-zA-Z0-9]{9,})')
        match = expr.match(barcode)
        if match is not None:
            match = match.group('barcode')
        else:
            match = ''
        return Scanner.ordinal_clean(match)
