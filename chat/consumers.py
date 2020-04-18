# chat/consumers.py
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
import json
from .models import Message, ChatRoom
from .views import update_last_message, other_user_party


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self,message):
        return {
            'author': message.author.username,
            'content': message.content,
            'time': str(datetime.strftime(message.timestamp, '%H:%M'))
        }

    def new_message(self,data):
        author = data['from']
        content = data['message']
        room_name = data['chat_room']
        author_user = get_object_or_404(User, username=author)
        current_time = datetime.strptime(data['current_time'], '%d-%m-%Y %H:%M:%S')
        message = Message.objects.create(author=author_user,
                                         content=content, chat_room=room_name, timestamp=current_time)
        update_last_message(room_name)
        party = other_user_party(author_user.id, room_name)
        room = ChatRoom.objects.get(name=room_name)
        if party == 'A':
            room.unread_A += 1
        elif party == 'B':
            room.unread_B += 1
        room.save()
        content = {
            'command': 'new_message',
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
        self.commands[data['command']](self,data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self,message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))











