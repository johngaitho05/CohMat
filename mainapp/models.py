from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model


User = get_user_model()


class Cohort(MPTTModel):
    title = models.CharField(max_length=250)
    logo = models.FileField(upload_to='group_logos')
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    no_of_members = models.IntegerField(default=0)
    total_posts = models.IntegerField(default=0)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    target_cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    content = models.TextField()
    total_answers = models.IntegerField(default=0)
    image = models.FileField(upload_to='images', blank=True, default='')

    def __str__(self):
        return self.author.username + ' >> ' + self.target_cohort.title


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)








