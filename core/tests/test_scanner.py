from django.test import TestCase

from core.scanner import Scanner


class ScannerTestCases(TestCase):
    # Tests `core.forms.Scanner.clean`
    def test_scannerordinalclean_match(self):
        self.assertEqual(Scanner.ordinal_clean('12341234123412\x03'), '12341234123412')
