from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile


@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'mainapp/home.html', {'active_link': 'home_link','user_profile': user_profile})


@login_required
def groupsView(request):
    return render(request, 'mainapp/groups.html',{'active_link':'groups_link'})


@login_required
def messagesView(request):
    return render(request, 'mainapp/messages.html',{'active_link':'messages_link'})


@login_required
def notificationsView(request):
    return render(request, 'mainapp/notifications.html',{'active_link':'notifications_link'})


# def askquestionView(request):
#     return render(request, 'mainapp/home.html',{'active_link':'question_link'})






















