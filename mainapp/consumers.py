import asyncio
import json
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
                    print(quiz_id)
                    question = Question.objects.filter(id=quiz_id).first()

                    """check whether the question being answered exists"""
                    if question:
                        recipient = question.author
                        new_room = f'room_{recipient.id}'
                        await self.channel_layer.group_add(new_room, self.channel_name)

                        # save the answer to database
                        await self.save_answer(author, question, ans)
                        # save the notification to database
                        notification_message = ''
                        if recipient != author:
                            notification_message = 'commented on your post'
                            await self.save_notification(author, recipient, notification_message)

                        ''' the content to be sent as notification'''
                        response = {
                            'command': notificationType,
                            'notifierUsername': author.username,
                            'notifierPhoto': author.userprofile.profile_photo.url,
                            'message': notification_message or None,
                            'quiz_id': quiz_id
                        }
                        # broadcasts the notification to be sent
                        await self.channel_layer.group_send(
                            new_room,
                            {
                                "type": "new_notification",
                                "text": json.dumps(response)
                            }
                        )
                elif notificationType == 'new_message':
                    chat_room = loaded_data.get('chat_room') or None
                    message  = loaded_data.get('message') or None
                    idNum = get_active_contact_id(author.id, chat_room)
                    if idNum and idNum != -1:
                        newRoom = f'room_{idNum}'
                        await self.channel_layer.group_add(newRoom, self.channel_name)
                        response = {
                            'command': notificationType,
                            'notifierName': reportingName,
                            'notifierPhoto': author.userprofile.profile_photo.url,
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
        print("disconnected", event)

    @database_sync_to_async
    def save_answer(self, author, question, answer):
        question.total_answers += 1
        question.save()
        return Answer.objects.create(author=author, question=question, content=answer)

    @database_sync_to_async
    def save_notification(self, author, recipient, content):
        recipient.userprofile.notifications_count += 1
        recipient.userprofile.save()
        return Notification.objects.create(author=author, recipient=recipient, content=content)
