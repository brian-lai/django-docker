from django_tables2 import columns


class ResourceStatisticsColumn(columns.Column):
    def __init__(self, *args, **kwargs):
        attr = kwargs.pop('attr', None)
        kwargs['order_by'] = 'statistics__date_created'
        super(ResourceStatisticsColumn, self).__init__(*args, **kwargs)

        # Make sure the user supplied an argument
        if attr is None:
            raise NotImplementedError('`%s` must declare \'attr\'' % self.__class__)
        self.accessor = 'get_statistics.' + attr
