from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'mainapp'

urlpatterns = [
     path('',HomeView.as_view(), name='homeView'),
     path('groups/', groupsView, name='groupsView'),
     path('messages/', messagesView, name='messagesView'),
     path('notifications/', notificationsView, name='notificationsView'),
     path('join/', join_groups, name='join')
  ]