from django import forms
from django.contrib.postgres import forms as pg_forms


class ScannerForm(forms.Form):
    barcode = forms.CharField(max_length=64)

    def clean_barcode(self):
        return self.cleaned_data['barcode'].strip()


class SingleObjectActionForm(forms.ModelForm):
    class Meta:
        fields = []

    perform = forms.BooleanField(widget=forms.HiddenInput())


class DisableSimpleArrayField(pg_forms.SimpleArrayField):
    def clean(self, value):
        # Corrects a bug that occurs when the field is disabled on the form
        if isinstance(value, list):
            return value

        return super(DisableSimpleArrayField, self).clean(value)
