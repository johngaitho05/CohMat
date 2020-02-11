from django.shortcuts import render


def home(request):
    return render(request, 'mainapp/homepage.html',{'active_link':'home_link'})


def groupsView(request):
    return render(request, 'mainapp/groups.html',{'active_link':'groups_link'})


def messagesView(request):
    return render(request, 'mainapp/messages.html',{'active_link':'messages_link'})


def notificationsView(request):
    return render(request, 'mainapp/notifications.html',{'active_link':'notifications_link'})


# def askquestionView(request):
#     return render(request, 'mainapp/homepage.html',{'active_link':'question_link'})