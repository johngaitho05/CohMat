import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

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
            # getting data from the fronted
            loaded_data = json.loads(data)
            notificationType = loaded_data.get('type')
            if notificationType == 'answer':
                ans = loaded_data.get('answer')
                quiz_id = int(loaded_data.get('questionId'))
                print(quiz_id)
                question = Question.objects.filter(id=quiz_id).first()

                """confirm that the question that the user is 
                answering exists and that the user is logged in"""
                if question and author.is_authenticated:
                    recipient = question.author
                    new_room = f'room_{recipient.id}'
                    await self.channel_layer.group_add(new_room, self.channel_name)

                    # save the answer to database
                    await self.save_answer(author, question, ans)
                    # save the notification to database
                    notification_message = author.first_name + ' ' + author.last_name + ' commented on your post'
                    await self.save_notification(recipient, notification_message)

                    ''' the content to be sent to included in the notification'''
                    response = {
                        'notifierUsername': author.username,
                        'recipientUsername': recipient.username,
                        'notifierPhoto': author.userprofile.profile_photo.url,
                        'message': notification_message
                    }
                    # broadcasts the notification to be sent
                    await self.channel_layer.group_send(
                        new_room,
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
    def save_notification(self, recipient, content):
        recipient.userprofile.notifications_count += 1
        recipient.userprofile.save()
        return Notification.objects.create(recipient=recipient, content=content)
