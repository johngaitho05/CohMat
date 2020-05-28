from django.db import models
from django.contrib.auth import get_user_model
from projectdir.utils import AgoTime

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    chat_room = models.CharField(max_length=50)
    deleted_A = models.BooleanField(default=False)
    deleted_B = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username

    def sliced_text(self):
        if len(self.content) > 40:
            return self.content[:40] + '...'
        else:
            return self.content

    def ago_time(self):
        return AgoTime(self.time)


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    last_message = models.ForeignKey(Message, null=True,
                                     related_name='chatroom_last_message',
                                     on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)
