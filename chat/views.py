from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Message, ChatRoom
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
from data_structures.Hashing.HashTable import HashTable
from data_structures.LinkedLists.DoublyLinkedList import DoublyLinkedList
from datetime import date, datetime
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
    party = other_user_party(request.user.id, room_name)
    update_unread(party, room_name)
    today = date.strftime(date.today(), "%Y-%m-%d")
    room_to_json = mark_safe(json.dumps(room_name))
    username_json = mark_safe(json.dumps(request.user.username))
    active_contact = get_active_contact(request.user.id, room_name)
    texts = Message.objects.filter(chat_room=room_name).order_by('-timestamp')
    texts_list = get_texts(texts)
    chat_list = get_recent_chats(request.user)
    if not texts_list:
        texts_list = 'Null'
    if chat_list is not None:
        return render(request, 'chat/home.html',
                      {'texts_list': texts_list,
                       'active_contact': active_contact,
                       'recents': chat_list[::-1],
                       'room_name':room_name,
                       'room_name_json': room_to_json,
                       'username_json': username_json,
                       'today': today})
    else:
        return render(request, 'chat/home.html',
                      {'texts_list': texts_list,
                       'active_contact': active_contact,
                       'recents': 'Null',
                       'room_name': room_name,
                       'room_name_json': room_to_json,
                       'username_json': username_json,
                       'today': today})


@login_required
def home(request):
    chat_list = get_recent_chats(request.user)
    if chat_list is not None:
        return render(request, 'chat/home.html', {'recents': chat_list})
    else:
        return render(request, 'chat/home.html', {'recents': 'Null'})


def contacts_view_extension(user):
    contacts = get_contacts(user)
    count = len(contacts)
    if count > 100:
        count = '99+ Contacts'
        contacts = contacts[0:100]
    elif count == 1:
        count = '1 Contact'
    else:
        count = str(count) + 'Contacts'
    return [get_chat_rooms(contacts, user), count]


# return a list of ids for those users that qualify to be in the user contacts
def get_contacts(user):
    to_compare = HashTable(27, user.userprofile.user_groups)
    other_users = User.objects.exclude(id=user.id)
    contacts = DoublyLinkedList()
    for user in other_users:
        user_groups = user.userprofile.user_groups
        for i in range(len(user_groups)):
            if to_compare.search(user_groups[i]) is not None:
                break
        contacts.insert_at_end(user.id)
    return contacts.display_list()


# returns a list of recent chats to display on the homepage
def get_recent_chats(user):
    contacts = get_contacts(user)
    contacts_list = [contact for contact in contacts]
    if len(contacts_list) > 0:
        chat_list = []
        for contact in contacts:
            room = get_chat_room(contact, user.id)
            if room.last_message != get_default_last_message():
                party = other_user_party(user.id,room.name)
                chat_list.append((User.objects.get(id=contact), room, room.last_message, party))
        if len(chat_list) == 0:
            return
        return chat_list
    return


# called when a new user registers to create chatrooms through which the user can chat with other members
def add_chat_rooms(current_user):
    users = User.objects.all()
    for user in users:
        new_room = str(user.id) + 'A' + str(current_user.id)
        ChatRoom.objects.create(name=new_room, last_message=get_default_last_message())


def get_chat_rooms(contacts, user):
    chat_rooms = []
    for contact in contacts:
        room = get_chat_room(contact, user.id)
        chat_rooms.append((User.objects.get(id=contact), room))
    return chat_rooms


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
            room = ChatRoom.objects.create(name=room_name, last_message=get_default_last_message())
    return room


def get_active_contact(user_id, chat_room):
    active_contact_id = get_active_contact_id(user_id, chat_room)
    active_contact = get_object_or_404(User, id=active_contact_id)
    return active_contact


def get_active_contact_id(user_id, chat_room):
    id_list = chat_room.split('A')
    if int(id_list[0]) == user_id:
        return int(id_list[1])
    elif int(id_list[1]) == user_id:
        return int(id_list[0])
    else:
        return -1


# updates the last message every time the text is sent to a given chatroom
def update_last_message(chat_room, message):
    current_room = ChatRoom.objects.get(name=str(chat_room))
    current_room.last_message = message
    current_room.save()


def other_user_party(user_id, chat_room):
    id_list = chat_room.split('A')
    if int(id_list[0]) == user_id:
        return 'B'
    elif int(id_list[1]) == user_id:
        return 'A'


def get_texts(messages):
    date_list = []
    texts_list = []
    for message in messages:
        message_date = str(message.timestamp)[:10]
        date_list.append(message_date)
    date_set = set(date_list)
    for message_date in date_set:
        texts = []
        for message in messages:
            if str(message.timestamp)[:10] == message_date:
                texts.append((message, str(message.timestamp)[10:16]))
        texts_list.append((message_date, texts[::-1]))
    return texts_list


def get_default_last_message():
    user = User.objects.get(username='johnyk')
    return Message.objects.filter(author=user, ).order_by('timestamp')[:1].get()


@login_required
def delete_texts(request):
    if request.method == 'POST':
        to_delete = request.POST.getlist('to_delete')
        for message_id in to_delete:
            message = Message.objects.get(id=int(message_id))
            message.delete()
        room_name = request.POST['room_name']
        return redirect('chat:chat', room_name=room_name)
    return redirect('chat:homepage')


def formatted_text(text):
    if len(text) > 40:
        return text[:40] + '...'
    else:
        return text


def update_unread(party, room_name):
    try:
        chat_room = ChatRoom.objects.get(name=room_name)
        if party == 'A':
            chat_room.unread_B = 0
        elif party == 'B':
            chat_room.unread_A = 0
        chat_room.save()
    except ChatRoom.DoesNotExist:
        ChatRoom.objects.create(name=room_name,last_message=get_default_last_message())



