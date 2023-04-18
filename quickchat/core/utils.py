from datetime import datetime, timedelta


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def add_to_date(in_date: datetime.date, time_format: str, value: int) -> datetime.date:
    """
    Adds a specific time value to the input date.

    :param in_date: The date you want to add time to.
    :param time_format: The time format you want to use, e.g 'days', 'hours'.
    :param value: The value for the time_format
    :return: the newly calculated date
    """
    kwargs = {time_format: value}

    return in_date + timedelta(**kwargs)


def now() -> datetime.date:
    """
    Returns the current time as date.
    :return:
    """
    return datetime.now()
