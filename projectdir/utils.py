import random
from datetime import datetime, date, timedelta
from django.template.defaultfilters import timesince, register
from django.utils import timezone
import pytz

from django.utils import timezone


class AgoTime:
    def __init__(self, date_time):
        ago = get_ago_time(date_time)
        if type(ago) != str or 'Yesterday' in ago:
            self.time = ago
        else:
            self.time = ago.replace(u'\xa0', ' ')

    def count(self):
        if type(self.time) == str:
            return int(self.time.split(' ')[0]) if 'Yesterday' not in self.time else None
        return

    def desc(self):
        if type(self.time) == str:
            return self.time[len(str(self.count())) + 1:] if 'Yesterday' not in self.time else None
        return

    def __str__(self):
        if type(self.time) == datetime:
            if timezone.now().year == self.time.year:
                return self.time.strftime("%d/%m at %H:%M")
            else:
                return self.time.strftime("%m/%Y")
        return self.time


@register.filter
def get_ago_time(passed_time):
    yesterday = timezone.now().date() - timedelta(days=1)
    diff = abs(passed_time - timezone.now())
    d = diff.days
    if d <= 30:
        span = timesince(passed_time)
        span = span.split(",")[0]  # just the most significant digit
        if passed_time.date() == yesterday:
            return "Yesterday at %s" % passed_time.strftime('%H:%M')
        return "%s ago" % span
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


def randomColor():
    letters = "0123456789ABCDEF"
    color = '#'
    for i in range(6):
        j = random.randint(0, 14)
        color += letters[j]
    return color if 'FF' not in color else randomColor()
