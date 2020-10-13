def filter_in(self, queryset, value):
    '''Takes a list as an argument and parses the JSON.
    '''
    value = eval(value)
    if isinstance(value, list):
        return queryset.filter(id__in=value)
    return queryset
