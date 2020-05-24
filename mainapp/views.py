import json
import random

from django.db.models import Count
from django.utils import timezone

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from chat.views import get_contacts, get_chat_rooms, get_chat_room
from chat.views import get_recent_chats, other_user_party
from .models import Cohort, Question, Notification, Answer, Reply
from accounts.models import UserProfile
from data_structures.Searching.Searching import binary_search
from data_structures.LinkedLists.SingleLinkedList import SingleLinkedList
from accounts.views import increment_group_members

local_tz = 'Africa/Nairobi'
timezone.activate(local_tz)


@method_decorator(login_required,
                  name='dispatch')
class HomeView(ListView):
    template_name = 'mainapp/home.html'
    context_object_name = 'quiz_and_ans'
    model = Question

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        data = get_user_data(self.request.user)
        today = timezone.now()
        yesterday = today - timezone.timedelta(days=1)
        context.update({
            'active_link': 'home_link',
            'to_recommend': data['to_recommend'],
            'contacts': data['contacts'],
            'user_cohorts': data['user_cohorts'],
            'today': today.date(),
            'yesterday': yesterday
        })
        return context

    def get_queryset(self):
        questions = get_user_data(self.request.user)['questions']
        qs = Question.objects.annotate(number_of_answers=Count('answer'))
        t = timezone.now()
        return [(q, Answer.objects.filter(question=q).order_by('-time')) for q in qs if q in questions]


@method_decorator(login_required, name='dispatch')
class GroupsView(ListView):
    template_name = 'mainapp/groups.html'
    context_object_name = 'cohorts_list'
    model = Cohort

    def get_context_data(self, **kwargs):
        data = get_user_data(self.request.user)
        context = super(GroupsView, self).get_context_data(**kwargs)
        context.update({
            'active_link': 'groups_link',
            'contacts': data['contacts']
        })
        return context

    def get_queryset(self):
        groups_to_display = get_cohorts(self.request.user)
        return groups_to_display


@login_required
def messagesView(request):
    data = get_user_data(request.user)
    messages = get_recent_chats(request.user)[::-1]
    return render(request, 'mainapp/messages.html',
                  {'active_link': 'messages_link',
                   'messages': messages,
                   'contacts': data['contacts']})


@method_decorator(login_required, name='dispatch')
class NotificationsView(ListView):
    template_name = 'mainapp/notifications.html'
    context_object_name = 'notifications'
    model = Notification

    def get_context_data(self, **kwargs):
        data = get_user_data(self.request.user)
        profile = self.request.user.userprofile
        profile.notifications_count = 0
        profile.save()
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context.update({
            'active_link': 'notifications_link',
            'contacts': data['contacts']
        })
        return context


@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    model = UserProfile
    template_name = 'mainapp/profile.html'

    def get_context_data(self, **kwargs):
        cohorts = [Cohort.objects.get(id=coh_id) for coh_id in self.request.user.userprofile.user_groups]
        context = super(ProfileView, self).get_context_data(**kwargs)
        chatroom = get_chat_room(UserProfile.objects.get(id=self.kwargs['pk']).user.id, self.request.user.id)
        context.update({
            'cohorts': cohorts,
            'chatroom': chatroom
        })
        return context


def get_user_data(user):
    contacts = get_contacts(user)  # fetches users to display at quick-chat pane
    user_cohorts = user.userprofile.user_groups  # IDs for cohorts that the user has joined
    user_cohorts = [Cohort.objects.get(id=cohort) for cohort in user_cohorts]  # getting real cohorts from the ids
    '''using a linked_list to dynamically store questions/posts that can be displayed to the user(newsfeed)'''
    questions_list = SingleLinkedList()
    # Iterate through all user_groups and get the last 100 posts for each
    for cohort in user_cohorts:
        questions = Question.objects.filter(target_cohort=cohort).order_by('-time')[:100]
        if questions:
            for q in questions:
                questions_list.insert_at_end(q.id)
    questions_list = sorted([Question.objects.get(id=int(quiz_id)) for
                             quiz_id in questions_list.display_list()], reverse=True)

    leaf_cohort = user.userprofile.study_field
    all_cohorts = leaf_cohort.get_descendants(include_self=False)
    to_recommend = []
    for cohort in all_cohorts:
        if cohort not in user_cohorts:
            to_recommend.append(cohort)
    random.shuffle(to_recommend)
    return {'to_recommend': to_recommend[:100], 'contacts': contacts,
            'questions': questions_list[:100], 'user_cohorts': user_cohorts}


@login_required
def join_groups(request, ):
    if request.method == 'POST':
        if request.POST.getlist('to_join'):
            to_join = [int(group_id) for group_id in request.POST.getlist('to_join')]
            user_groups = request.user.userprofile.user_groups
            for group_id in to_join:
                user_groups.append(group_id)
            new_user_groups_list = user_groups
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.user_groups = new_user_groups_list
            user_profile.save()
            increment_group_members(to_join)
            page = request.POST['page']
            if page == 'home':
                return redirect('mainapp:homeView')
            else:
                return redirect('mainapp:groupsView')

    return redirect('mainapp:homeView')


def get_cohorts(user):
    user_cohorts = user.userprofile.user_groups
    all_cohorts = Cohort.objects.all()
    cohorts_list = [cohort.id for cohort in all_cohorts]
    to_recommend = SingleLinkedList()
    for coh_id in cohorts_list:
        if binary_search(coh_id, user_cohorts) is None:
            to_recommend.insert_at_end(coh_id)
    to_recommend = [Cohort.objects.get(id=coh_id) for coh_id in to_recommend.display_list()]
    random.shuffle(to_recommend)
    return to_recommend[0:30]


@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST['question-text']
        target_group_id = request.POST['question-group']
        target_group = Cohort.objects.get(id=int(target_group_id))
        try:
            image = request.FILES['question-image']
            handle_uploaded_file(image, 'images')
            Question.objects.create(author=request.user, content=content,
                                    image='images' + '/' + image.name, target_cohort=target_group)
        except MultiValueDictKeyError:
            Question.objects.create(author=request.user, content=content, target_cohort=target_group)
        return redirect('mainapp:homeView')


@login_required
def add_answer(request):
    if request.method == 'POST':
        content = request.POST['answer']
        author = request.user
        question = Question.objects.get(id=int(request.POST['question']))
        new_answer = Answer(content=content, author=author, question=question)
        new_answer.save()
        question.total_answers += 1
        question.save()

    return redirect('mainapp:homeView')


# saving the uploaded media file
def handle_uploaded_file(file, desired_location):
    with open(settings.MEDIA_ROOT + '/' + desired_location + '/' + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)



