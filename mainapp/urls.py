from django.urls import path
from .views import *

app_name = 'mainapp'

urlpatterns = [
     path('', home, name='homeView'),
     path('groups', groupsView, name='groupsView'),
     path('mesages', messagesView, name='messagesView'),
     path('notifications', notificationsView, name='notificationsView'),
     # path('ask_question', askquestionView, name='askquestionView')
  ]