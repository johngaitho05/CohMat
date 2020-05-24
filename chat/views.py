from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import UserProfile
from .models import Contact, Message, ChatRoom
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
from data_structures.Hashing.HashTable import HashTable
from data_structures.Queue.PriorityQueue import PriorityQueue
from datetime import date, datetime, timedelta
from django.utils.safestring import mark_safe
import json


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
    room = get_object_or_404(ChatRoom, name=room_name)
    party = other_user_party(request.user.id, room_name)
    update_unread(party, room_name)
    today = date.today()
    yesterday = today - timedelta(1)
    room_to_json = mark_safe(json.dumps(room_name))
    username_json = mark_safe(json.dumps(request.user.username))
    active_contact = get_active_contact(request.user.id, room_name)
    texts_list = get_texts(room_name)
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
                       'yesterday': yesterday})
    else:
        return render(request, 'chat/home.html',
                      {'texts_list': texts_list,
                       'active_contact': active_contact,
                       'recents': 'Null',
                       'room_name': room_name,
                       'room_name_json': room_to_json,
                       'username_json': username_json,
                       'today': today,
                       'yesterday': yesterday})


@login_required
def home(request):
    chat_list = get_recent_chats(request.user)
    if chat_list:
        return render(request, 'chat/home.html', {'recents': chat_list})
    else:
        return render(request, 'chat/home.html', {'recents': 'Null'})


def contacts_view_extension(user):
    contacts = get_contacts(user)
    count = len(contacts)
    if count > 100:
        count = '99+ Contacts'
        contacts = contacts[:100]
    elif count == 1:
        count = '1 Contact'
    else:
        count = str(count) + 'Contacts'
    return [get_contacts(user), count]


# return a list of ids for those users that qualify to be in the user contacts
def get_contacts(user):
    contacts = User.objects.filter(userprofile__study_field=user.userprofile.study_field)
    contacts_list = [contact for contact in contacts if contact != user]
    return get_chat_rooms(contacts_list, user)


# returns a list of recent chats to display on the homepage
def get_recent_chats(user):
    recent_chat_rooms = ChatRoom.objects.filter(name__contains=str(user.id),
                                                last_message__timestamp__year=datetime.today().year)
    recent_chat_rooms = recent_chat_rooms.order_by('-last_message_id',)[:20]
    chat_list = [chat_room for chat_room in recent_chat_rooms]
    for i in range(len(chat_list)):
        chat_room = chat_list[i]
        contact = get_active_contact(user.id, chat_room.name)
        party = other_user_party(user.id, chat_room.name)
        last_text = chat_room.last_message
        chat_list[i] = (contact, chat_room, party, last_text)
    return chat_list


# called when a new user registers to create chatrooms through which the user can chat with other members
def add_chat_rooms(current_user):
    users = User.objects.all()
    for user in users:
        new_room = str(user.id) + 'A' + str(current_user.id)
        ChatRoom.objects.create(name=new_room)


def get_chat_rooms(contacts, user):
    for i in range(len(contacts)):
        room = get_chat_room(contacts[i].id, user.id)
        contacts[i] = (contacts[i], room)
    return contacts


def get_chat_room(contact_id, user_id):
    if contact_id < user_id:
        room_name = str(contact_id) + 'A' + str(user_id)
    else:
        room_name = str(user_id) + 'A' + str(contact_id)
    try:
        room = ChatRoom.objects.get(name=room_name)
    except ChatRoom.DoesNotExist:
        chatroom_messages = Message.objects.filter(chat_room=room_name).order_by('-timestamp')
        if chatroom_messages:
            messages_list = [message for message in chatroom_messages]
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
        if int(id_list[0]) == user_id:
            return int(id_list[1])
        elif int(id_list[1]) == user_id:
            return int(id_list[0])
    return -1


def other_user_party(user_id, room_name):
    id_list = room_name.split('A')
    if int(id_list[0]) == user_id:
        return 'B'
    elif int(id_list[1]) == user_id:
        return 'A'


def get_texts(room_name):
    messages = Message.objects.filter(chat_room=room_name)
    date_list = [message.timestamp.date() for message in messages]
    date_set = sorted(set(date_list))
    texts_list = [None] * len(date_set)
    for i in range(len(date_set)):
        message_date = date_set[i]
        texts = [(message, message.timestamp.time()) for message in messages if
                 message.timestamp.date() == message_date]
        texts_list[i] = (message_date, texts)
    return texts_list


@login_required
def delete_texts(request):
    if request.method == 'POST':
        to_delete = request.POST.getlist('to_delete')
        for message_id in to_delete:
            message = Message.objects.get(id=int(message_id))
            message.delete()
        room_name = request.POST['room_name']
        update_last_message(room_name)
        return redirect('chat:chat', room_name=room_name)
    return redirect('chat:homepage')


def update_unread(party, room_name):
    try:
        chat_room = ChatRoom.objects.get(name=room_name)
        if party == 'A':
            chat_room.unread_B = 0
        elif party == 'B':
            chat_room.unread_A = 0
        chat_room.save()
    except ChatRoom.DoesNotExist:
        ChatRoom.objects.create(name=room_name)


# updates the last message every time the text is sent to a given chatroom
def update_last_message(room_name):
    try:
        chat_room = ChatRoom.objects.get(name=room_name)
        message = Message.objects.filter(chat_room=chat_room).order_by('-timestamp').first()
        chat_room.last_message = message
        chat_room.save()
    except ChatRoom.DoesNotExist:
        print("Chat_room not found!")
