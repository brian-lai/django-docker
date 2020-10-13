from django.utils.functional import lazy


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    @staticmethod
    def write(value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def assert_ordered_listview_querysets(module):
    import inspect
    import importlib
    unordered_querysets = []
    # import the module and iterate through all classes
    for _, obj in inspect.getmembers(importlib.import_module(module), inspect.isclass):
        # check only classes defined in the module (vs imported from other modules)
        if obj.__module__ == module and 'List' in obj.__name__ and hasattr(obj, 'queryset'):
            if hasattr(obj.queryset, '_ordering') and not obj.queryset._ordering \
               or hasattr(obj.queryset, 'ordered') and not obj.queryset.ordered:
                unordered_querysets.append(
                    'queryset in list view {}.{} is unordered'.format(obj.__module__, obj.__name__)
                )
    return unordered_querysets


def _lazy_format(string, *args, **kwargs):
    """
    Helper function for lazy string formatting
    """
    return string.format(*args, **kwargs)
lazy_format = lazy(_lazy_format, str)
