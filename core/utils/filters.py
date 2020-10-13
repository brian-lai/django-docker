import django_filters


class DateCreatedFilter(django_filters.DateFilter):
    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'statistics__date_created'
        super(DateCreatedFilter, self).__init__(*args, **kwargs)


class DateCreatedRangeFilter(django_filters.DateRangeFilter):
    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'statistics__date_created'
        super(DateCreatedRangeFilter, self).__init__(*args, **kwargs)
