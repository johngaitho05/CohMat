from django.db import models
from django.contrib.auth import get_user_model
import os
from projectdir import settings

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='profile_photos',
                                     default = os.path.join(settings.MEDIA_ROOT,
                                                            'profile_photos/default_profile_pic.png'), )
    study_field = models.CharField(max_length=250)
    user_groups = models.TextField(default='[]')

    def __str__(self):
        return self.user.username


