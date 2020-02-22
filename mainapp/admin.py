from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

admin.site.register(Cohort, MPTTModelAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Reply)
admin.site.register(Notification)
