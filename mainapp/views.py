from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import *
from chat.views import get_contacts, get_chat_rooms

from .models import Cohort, Question, Notification, Answer, Reply
from accounts.models import UserProfile
from django.contrib.auth.models import User


@method_decorator(login_required,
                  name='dispatch')
class HomeView(ListView):
    template_name = 'mainapp/home.html'
    context_object_name = 'questions_list'
    model = Question

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        data = get_user_data(self.request.user)
        context.update({
            'to_recommend': data[0],
            'connected_people_list': data[1],
            'contacts': data[2]
        })
        return context

    def get_queryset(self):
        return Question.objects.all()


@login_required
def groupsView(request):
    return render(request, 'mainapp/groups.html', {'active_link': 'groups_link'})


@login_required
def messagesView(request):
    return render(request, 'mainapp/messages.html', {'active_link': 'messages_link'})


@login_required
def notificationsView(request):
    return render(request, 'mainapp/notifications.html', {'active_link': 'notifications_link'})


def get_user_data(user):
    contacts_ids = get_contacts(user)
    contacts = get_chat_rooms(contacts_ids,user)
    user_cohorts = user.userprofile.user_groups
    user_cohorts = [Cohort.objects.get(id=cohort) for cohort in user_cohorts]
    leaf_cohort = Cohort.objects.get(id=user.userprofile.study_field)
    all_cohorts = leaf_cohort.get_descendants(include_self=False)
    to_recommend = []
    for cohort in all_cohorts:
        if cohort not in user_cohorts:
            to_recommend.append(cohort)
    to_recommend = to_recommend
    return [to_recommend, User.objects.all(),contacts]


@login_required
def join_groups(request,):
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
            for group_id in to_join:
                group = get_object_or_404(Cohort, id=group_id)
                group.no_of_members = group.no_of_members+1
                group.save()

            return render(request, 'mainapp/home.html',{
                'to_recommend': get_user_data(request.user)[0],
                'connected_people_list': get_user_data(request.user)[1],
                'message': 'You have successfully joined the selected groups'
            })

    return redirect('mainapp:homeView')




