from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from projectdir.utils import AgoTime

User = get_user_model()


class Cohort(MPTTModel):
    title = models.CharField(max_length=100, unique=True)
    logo = models.FileField(upload_to='group_logos', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='cohorts', related_query_name='cohort')

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    target_cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images', blank=True, default='')

    def ago_time(self):
        return AgoTime(self.time)

    def __str__(self):
        return self.author.username + ' >> ' + self.target_cohort.title


class Notification(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifier')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='toNotify')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    def ago_time(self):
        return AgoTime(self.time)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def ago_time(self):
        return AgoTime(self.time)


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def ago_time(self):
        return AgoTime(self.time)
