from datetime import datetime, date, timedelta
from django.template.defaultfilters import timesince, register
from django.utils import timezone
import pytz

from django.utils import timezone


class AgoTime:
    def __init__(self, date_time):
        self.time = get_ago_time(date_time).replace(u'\xa0', ' ')

    def count(self):
        return int(self.time.split(' ')[0])

    def desc(self):
        return self.time[len(str(self.count())) + 1:]

    def __str__(self):
        return self.time


@register.filter
def get_ago_time(passed_time):
    diff = abs(passed_time - timezone.now())
    if diff.days <= 0:
        span = timesince(passed_time)
        span = span.split(",")[0]  # just the most significant digit
        if span == "0 minutes":
            return "seconds ago"
        return "%s ago" % span
    return date(passed_time)


class CustomTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('custom_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
