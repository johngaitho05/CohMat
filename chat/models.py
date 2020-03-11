
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(User, related_name="user_contacts",on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(User, related_name="user_messages",on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()
    chat_room = models.CharField(max_length=50)

    def __str__(self):
        return self.author.username

    def sliced_text(self):
        if len(self.content) > 40:
            return self.content[:40] + '...'
        else:
            return self.content


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    last_message = models.ForeignKey(Message, related_name='chatroom_last_message'
                                     , on_delete=models.CASCADE)
    unread_A = models.IntegerField(default=0)
    unread_B = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)








