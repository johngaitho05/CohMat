# chat/consumers.py
from time import timezone

from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
import json

from django.utils.timezone import make_aware

from .models import Message, ChatRoom
from .views import update_last_message, other_user_party, get_active_contact

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        author = self.scope['user']
        return {
            'id': message.pk,
            'authorUsername': author.username,
            'reportingName': author.first_name + ' ' + author.last_name,
            'authorImage': author.userprofile.profile_photo.url,
            'content': message.content,
            'time': str(datetime.strftime(message.time, '%H:%M'))
        }

    def new_message(self, data):
        content = data['message']
        room_name = data['chat_room']
        time_string = data['current_time']
        current_time = datetime.strptime(time_string, '%d-%m-%Y %H:%M:%S')
        author_user = self.scope['user']
        if author_user.is_authenticated:
            message = Message.objects.create(author=author_user, content=content, chat_room=room_name,
                                             time=current_time)
            update_last_message(room_name)
            recipient = get_active_contact(author_user.id, room_name)
            print(recipient)
            content = {
                'command': 'new_message',
                'author': author_user.username,
                'message': self.message_to_json(message),
                'last_text': message.sliced_text()
            }
            self.send_chat_message(content)

    commands = {
        # 'fetch_messages':fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.accept())

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
