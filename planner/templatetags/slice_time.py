from django.template import Library
from datetime import datetime
from datetime import timedelta

register = Library()


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


@register.filter
def slice_time(value=None):
    """
    Filter -- returns a list of datetimes between fixed dates,
    sliced by a number of slices
    """
    start_hour = 8
    end_hour = 18
    if value == 1:
        value = (end_hour-start_hour)*4
    current_date = datetime.now()
    start_date = current_date.replace(
        hour=start_hour,
        minute=0,
        second=0,
        microsecond=0
    )
    end_date = current_date.replace(
        hour=end_hour,
        minute=0,
        second=0,
        microsecond=0
    )
    difference = end_date - start_date
    sliced_by = timedelta(seconds=difference.total_seconds()/value)
    end_date = end_date + sliced_by
    return (result for result in perdelta(start_date, end_date, sliced_by))
