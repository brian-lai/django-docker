def get_date_display(attr):
        if attr is not None:
            return attr.strftime('%b. %d %Y')
        return ''


def get_datetime_display(attr):
    if attr is not None:
        return attr.strftime('%b. %d %Y, %I:%M%p')
    return ''
