import asyncio
import json

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from chat.views import get_active_contact_id
from mainapp.models import Notification, Question, Answer


class NotificationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        user = self.scope['user']
        if user.is_authenticated:
            room = f"room_{user.id}"
            self.room = room
            await self.channel_layer.group_add(
                room,
                self.channel_name
            )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        data = event.get('text', None)
        if data is not None:
            author = self.scope['user']
            reportingName = author.first_name + ' ' + author.last_name
            # getting data from the fronted
            loaded_data = json.loads(data)
            notificationType = loaded_data.get('command')
            if author.is_authenticated:
                if notificationType == 'new_answer':
                    ans = loaded_data.get('answer')
                    quiz_id = int(loaded_data.get('questionId'))
                    question = Question.objects.filter(id=quiz_id).first()

                    """check whether the question being answered exists"""
                    if question:
                        recipient = question.author
                        new_room = f'room_{recipient.id}'
                        await self.channel_layer.group_add(new_room, self.channel_name)

                        # save the answer to database
                        await self.save_answer(author, question, ans)
                        # save the notification to database
                        if recipient != author:
                            notification_description = 'commented on your post'
                            await self.save_notification(author, recipient, 'NC', notification_description)

                        ''' the content to be sent as notification'''
                        response = {
                            'reportingName': reportingName,
                            'command': notificationType,
                            'notifierUsername': author.username,
                            'notifierPhoto': author.userprofile.profile_photo.url,
                            'content': ans if ans else '',
                            'quizId': quiz_id
                        }
                        # broadcasting the notification
                        await self.channel_layer.group_send(
                            new_room,
                            {
                                "type": "new_notification",
                                "text": json.dumps(response)
                            }
                        )
                elif notificationType == 'new_message':
                    chat_room = loaded_data.get('chat_room') or None
                    message = loaded_data.get('message') or None
                    idNum = get_active_contact_id(author.id, chat_room)
                    if idNum and idNum != -1:
                        recipient = await self.get_user(idNum)
                        await self.save_notification(author, recipient, 'NM', message)
                        newRoom = f'room_{idNum}'
                        await self.channel_layer.group_add(newRoom, self.channel_name)
                        response = {
                            'command': notificationType,
                            'notifierName': reportingName,
                            'notifierPhoto': await self.get_profile_photo_url(author),
                            'message': message
                        }
                        # broadcasts the notification to be sent
                        await self.channel_layer.group_send(
                            newRoom,
                            {
                                "type": "new_notification",
                                "text": json.dumps(response)
                            }
                        )


    async def new_notification(self, event):
        # sends the notification to the target party
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room,
            self.channel_name
        )
        raise StopConsumer()

    @database_sync_to_async
    def get_profile_photo_url(self,author):
        return author.userprofile.profile_photo.url

    @database_sync_to_async
    def get_user(self,idNum):
        return User.objects.get(pk=idNum)

    @database_sync_to_async
    def save_answer(self, author, question, answer):
        return Answer.objects.create(author=author, question=question, content=answer)

    @database_sync_to_async
    def save_notification(self, author, recipient, category, description):
        return Notification.objects.create(author=author, recipient=recipient, category=category,
                                           description=description)
