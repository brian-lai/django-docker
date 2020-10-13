from django.contrib.auth.models import User
from django.test import TestCase

from core.forms import ScannerForm, SingleObjectActionForm


class UserActionForm(SingleObjectActionForm):
    class Meta(SingleObjectActionForm.Meta):
        model = User


class FormTestCases(TestCase):
    # Tests `core.forms.ScannerForm`
    def test_scannerform(self):
        form = ScannerForm({'barcode': '  12341234123412   '})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['barcode'], '12341234123412')

    # Tests `core.forms.SingleObjectActionForm`
    def test_valid_singleobjectactionform(self):
        form = UserActionForm({'perform': 'true'})
        form.Meta.model = User
        self.assertTrue(form.is_valid())

    # Tests `core.forms.SingleObjectActionForm`
    def test_invalid_singleobjectactionform(self):
        form = UserActionForm({})
        form.Meta.model = User
        self.assertFalse(form.is_valid())
