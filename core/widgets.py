from django.forms import TextInput


class BarcodeWidget(TextInput):
    '''Form field which automatically adds the proper angular bindings for the scanner component.
    '''
    def build_attrs(self, *args, **kwargs):
        attrs = super(BarcodeWidget, self).build_attrs(*args, **kwargs)
        attrs.update({
            'barcode-field': '',
        })
        return attrs
