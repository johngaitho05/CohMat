from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='profile_photos',
                                     default='settings.MEDIA_ROOT/profile_photos/avatar_default.jpg')
    study_field = models.CharField(max_length=250)
    user_groups = models.TextField()