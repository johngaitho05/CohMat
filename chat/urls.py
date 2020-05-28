from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
     path('', views.home, name='homepage'),
     path('contacts', views.contacts_view, name='show_contacts'),
     path('delete',views.delete_texts,name='delete_texts'),
     path('chat/<str:room_name>', views.chat, name='chat'),
     path('mark-as-read', views.mark_as_read, name='mark_as_read'),

]