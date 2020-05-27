from django.urls import path

from accounts.views import update_profile
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'mainapp'

urlpatterns = [
     path('', HomeView.as_view(), name='homeView'),
     path('groups/', GroupsView.as_view(), name='groupsView'),
     path('messages/', messagesView, name='messagesView'),
     path('notifications/', NotificationsView.as_view(), name='notificationsView'),
     path('join/', join_groups, name='join'),
     path('new-post', create_post, name='create_post'),
     path('answer_quiz', add_answer, name='answer_quiz'),
     path('user_profile/<int:pk>', ProfileView.as_view(), name='profile_view'),
     path('user_profile/update', update_profile, name='profile_update'),
  ]