from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
import os
import json
from projectdir import settings
from mainapp.models import Cohort

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='profile_photos',
                                     default=os.path.join(settings.MEDIA_ROOT,
                                                          'profile_photos/default_profile_pic.png'), )
    study_field = models.ForeignKey(Cohort, on_delete=models.DO_NOTHING)
    user_groups = ArrayField(models.IntegerField(), null=True, blank=True)
    current_interest = models.ForeignKey(Cohort, on_delete=models.DO_NOTHING, null=True,
                                         related_name='user_current_interest')
    school = models.CharField(max_length=250)
    bio = models.TextField(null=True)
    messages_count = models.IntegerField(default=0)
    notifications_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
