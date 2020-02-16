from django.contrib import admin
from .models import *

admin.site.register(Cohort)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Reply)
admin.site.register(Notification)
