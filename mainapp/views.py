from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import *
from sqlparse.engine.grouping import group_aliased

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
        context.update({
            'to_recommend': user_data(self.request.user)[0],
            'connected_people_list': user_data(self.request.user)[1]
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


def user_data(user):
    user_cohorts = user.userprofile.user_groups
    user_cohorts = [Cohort.objects.get(id=cohort) for cohort in user_cohorts]
    leaf_cohort = Cohort.objects.get(id=user.userprofile.study_field)
    all_cohorts = leaf_cohort.get_descendants(include_self=False)
    to_recommend = []
    for cohort in all_cohorts:
        if cohort not in user_cohorts:
            to_recommend.append(cohort)
    to_recommend = to_recommend
    return [to_recommend, User.objects.all()]


@login_required
def join_groups(request):
    if request.method == 'POST':
        if request.POST.getlist('to_join'):
            user_groups = request.user.userprofile.user_groups
            to_join = request.POST.getlist('to_join')
            for group_id in to_join:
                user_groups.append(int(group_id))
            new_user_groups_list = user_groups
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.user_groups = new_user_groups_list
            user_profile.save()
            return render(request, 'mainapp/home.html',{
                'to_recommend': user_data(request.user)[0],
                'connected_people_list': user_data(request.user)[1],
                'message': 'You have successfully joined the selected groups'
            })

    return redirect('mainapp:homeView')




