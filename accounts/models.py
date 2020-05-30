from django.contrib.postgres.fields import ArrayField
import os
from django.db import models
from django.contrib.auth import get_user_model
from projectdir import settings
from mainapp.models import Cohort

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='profile_photos',
                                     default=os.path.join(settings.MEDIA_ROOT,
                                                          'profile_photos/default_profile_pic.png'), )
    study_field = models.ForeignKey(Cohort, on_delete=models.DO_NOTHING, related_name='study_field')
    user_cohorts = models.ManyToManyField(Cohort, related_name='user_cohorts')
    current_interest = models.ForeignKey(Cohort, on_delete=models.DO_NOTHING, null=True,
                                         related_name='user_current_interest')
    school = models.CharField(max_length=250)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.user.username
