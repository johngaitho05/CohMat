from datetime import datetime, date, timedelta
from django.template.defaultfilters import timesince, register
from django.utils import timezone
import pytz

from django.utils import timezone


class AgoTime:
    def __init__(self, date_time):
        ago = get_ago_time(date_time)
        if type(ago) != str:
            print('not a string!!')
            self.time = ago
        else:
            self.time = ago.replace(u'\xa0', ' ')

    def count(self):
        return int(self.time.split(' ')[0]) if type(self.time) == str else None

    def desc(self):
        return self.time[len(str(self.count())) + 1:] if type(self.time) == str else None

    def __str__(self):
        return self.time


@register.filter
def get_ago_time(passed_time):
    diff = abs(passed_time - timezone.now())
    d = diff.days
    if d <= 0:
        span = timesince(passed_time)
        span = span.split(",")[0]  # just the most significant digit
        return "%s ago" % span
    elif d == 1:
        return '1 day ago'
    return passed_time


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
