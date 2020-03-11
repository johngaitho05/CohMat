from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
     path('contacts', views.contacts_view, name='show_contacts'),
     path('delete',views.delete_texts,name='delete_texts'),
     path('chat/<str:room_name>', views.chat, name='chat'),
     path('', views.home, name='homepage'),
]