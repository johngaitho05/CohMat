from datetime import datetime, date, timedelta
from django.template.defaultfilters import timesince, register
from django.utils import timezone


@register.filter
def ago(date_time):
    diff = abs(date_time - timezone.now())
    if diff.days <= 0:
        span = timesince(date_time)
        span = span.split(",")[0]  # just the most significant digit
        if span == "0 minutes":
            return "seconds ago"
        return "%s ago" % span
    return date(date_time)