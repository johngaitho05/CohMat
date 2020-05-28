import json
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.utils.safestring import mark_safe
from .models import Message, ChatRoom


@login_required
def contacts_view(request):
    chatrooms = contacts_view_extension(request.user)
    if not chatrooms[0]:
        return render(request, 'chat/home.html',
                      {'count': chatrooms[1], 'message': 'You have not added any contact'})
    else:
        return render(request, 'chat/home.html',
                      {'count': chatrooms[1], 'contacts': chatrooms[0]})


@login_required
def chat(request, room_name):
    active_contact = get_active_contact(request.user.id, room_name)
    party = other_user_party(request.user.id, room_name)
    updateRead(room_name, get_active_contact(request.user.id, room_name))
    today = date.today()
    yesterday = today - timedelta(1)
    room_to_json = mark_safe(json.dumps(room_name))
    username_json = mark_safe(json.dumps(request.user.username))
    texts_list = get_texts(room_name, request.user)
    chat_list = get_recent_chats(request.user)
    if not texts_list:
        texts_list = 'Null'
    if chat_list:
        return render(request, 'chat/home.html',
                      {'texts_list': texts_list,
                       'active_contact': active_contact,
                       'recents': chat_list[::-1],
                       'room_name': room_name,
                       'room_name_json': room_to_json,
                       'username_json': username_json,
                       'today': today,
                       'yesterday': yesterday,
                       'party': party,
                       })

    else:
        return render(request, 'chat/home.html',
                      {'texts_list': texts_list,
                       'active_contact': active_contact,
                       'recents': 'Null',
                       'room_name': room_name,
                       'room_name_json': room_to_json,
                       'username_json': username_json,
                       'today': today,
                       'yesterday': yesterday,
                       'party': party
                       })


@login_required
def home(request):
    chat_list = get_recent_chats(request.user)
    if chat_list:
        return render(request, 'chat/home.html', {'recents': chat_list})
    else:
        return render(request, 'chat/home.html', {'recents': 'Null'})


def contacts_view_extension(user):
    contacts = get_contacts(user)[0]
    count = len(contacts)
    if count > 100:
        count = '99+ Contacts'
        contacts = contacts[:100]
    elif count == 1:
        count = '1 Contact'
    else:
        count = str(count) + 'Contacts'
    return [contacts, count]


# return a list of ids for those users that qualify to be in the user contacts
def get_contacts(user):
    try:
        contacts = User.objects.filter(userprofile__study_field=user.userprofile.study_field)
    except UserProfile.DoesNotExist:
        print('User does not have a profile')
        raise Http404('Ops! Something went wrong')
    contacts_list = [contact for contact in contacts if contact != user]
    return get_chat_rooms(contacts_list, user)


# returns a list of recent chats to display on the homepage
def get_recent_chats(user):
    recent_rooms = ChatRoom.objects.filter(name__endswith=f'A{user.id}', last_message__isnull=False)
    if not recent_rooms:
        recent_rooms = ChatRoom.objects.filter(name__startswith=f'{user.id}A')
    recent_rooms = recent_rooms.order_by('-last_message_id', )[:100]
    chat_list = [chat_room for chat_room in recent_rooms]
    for i in range(len(chat_list)):
        chat_room = chat_list[i]
        contact = get_active_contact(user.id, chat_room.name)
        if contact:
            party = other_user_party(user.id, chat_room.name)
            messages = None
            if party == 'A':
                messages = Message.objects.filter(chat_room=chat_room.name, deleted_B=False).order_by('id')
            elif party == 'B':
                messages = Message.objects.filter(chat_room=chat_room.name, deleted_A=False).order_by('id')
            last_text = messages.last() if messages else None
            unread = Message.objects.filter(chat_room=chat_room.name, author=contact, read=False).count()
            chat_list[i] = (contact, chat_room, last_text, unread) if messages else None
        else:
            chat_list[i] = None
    return [recent for recent in chat_list if recent]


# called when a new user registers to create chatrooms through which the user can chat with other members
def add_chat_rooms(current_user):
    users = User.objects.exclude(current_user)
    users = [user for user in users if user is not current_user]
    if users:
        for user in users:
            new_room = str(user.id) + 'A' + str(current_user.id)
            ChatRoom.objects.create(name=new_room)


def get_chat_rooms(contacts, user):
    total_unread = 0
    for i in range(len(contacts)):
        contact = contacts[i]
        room = get_chat_room(contact.id, user.id)
        contacts[i] = (contact, room)
        unread = Message.objects.filter(chat_room=room.name, author=contact, read=False).count()
        total_unread += unread
    return [contacts, total_unread]


def get_chat_room(contact_id, user_id):
    if contact_id < user_id:
        room_name = str(contact_id) + 'A' + str(user_id)
    else:
        room_name = str(user_id) + 'A' + str(contact_id)
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        chat_room_messages = Message.objects.filter(chat_room=room_name).order_by('-time')
        if chat_room_messages:
            messages_list = [message for message in chat_room_messages]
            room = ChatRoom.objects.create(name=room_name, last_message=messages_list[0])
        else:
            room = ChatRoom.objects.create(name=room_name)
    return room


def get_active_contact(user_id, room_name):
    active_contact_id = get_active_contact_id(user_id, room_name)
    active_contact = get_object_or_404(User, id=active_contact_id)
    return active_contact


def get_active_contact_id(user_id, room_name):
    if user_id and room_name:
        id_list = room_name.split('A')
        if len(id_list) != 2:
            return -1
        try:
            id_list = [int(Id) for Id in id_list]
            if id_list[0] == user_id:
                return id_list[1]
            elif id_list[1] == user_id:
                return int(id_list[0])
            return -1
        except ValueError:
            return -1
    return -1


def other_user_party(user_id, room_name):
    id_list = room_name.split('A')
    if int(id_list[0]) == user_id:
        return 'B'
    elif int(id_list[1]) == user_id:
        return 'A'
    return


# Getting actual messages that will appear on the chat panel
def get_texts(room_name, user):
    party = other_user_party(user.id, room_name)
    messages = Message.objects.filter(chat_room=room_name).order_by('id')
    date_list = [message.time.date() for message in messages]
    date_set = sorted(set(date_list))
    texts_list = [None] * len(date_set)
    for i in range(len(date_set)):
        message_date = date_set[i]
        texts = [message for message in messages if message.time.date() ==
                 message_date and not message_is_deleted(message, party)]

        texts_list[i] = (message_date, texts) if texts else None
        for j in range(len(texts_list)):
            if texts_list[j] is None:
                texts_list.pop(j)
    return texts_list


def message_is_deleted(message, party):
    if party == 'A' and message.deleted_B or party == 'B' and message.deleted_A:
        return True
    return False


@csrf_exempt
def mark_as_read(request):
    if request.is_ajax():
        msgId = request.POST['msgId']
        if msgId:
            message = get_object_or_404(Message, id=msgId)
            message.read = True
            message.save()
            return JsonResponse({'message': 'marked as read'})
        return JsonResponse({'message': 'Could not mark as read. Required msgId parameter not found'})
    return redirect('chat:homepage')


@login_required
def delete_texts(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        to_delete = request.POST.getlist('to_delete')
        party = other_user_party(request.user.id, room_name)
        print(party)
        room = ChatRoom.objects.filter(name=room_name).first()
        if room:
            if party == 'A':
                for message_id in to_delete:
                    message = Message.objects.get(id=int(message_id))
                    if message.deleted_A:
                        message.delete()
                    else:
                        message.deleted_B = True
                        message.save()
            else:
                for message_id in to_delete:
                    message = Message.objects.get(id=int(message_id))
                    if message.deleted_B:
                        message.delete()
                    else:
                        message.deleted_A = True
                        message.save()
            update_last_message(room_name)
            return redirect('chat:chat', room_name=room_name)
        print('No such ChatRoom')
        raise Http404('Something went wrong')
    return redirect('chat:homepage')


def updateRead(room_name, user):
    messages = Message.objects.filter(chat_room=room_name, author=user, read=False)
    if messages:
        for message in messages:
            message.read = True
            message.save()


# updates the last message every time the text is sent to a given chatroom
def update_last_message(room_name):
    try:
        chat_room = ChatRoom.objects.get(name=room_name)
        message = Message.objects.filter(chat_room=chat_room, ).order_by(
            '-time').first()
        chat_room.last_message = message
        chat_room.save()
    except ChatRoom.DoesNotExist:
        print("Chat_room not found!")
