from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from chat.views import add_chat_rooms
from .models import *
from mainapp.models import *
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        study_field = request.POST['study_field']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        groups = request.POST['groups']
        profile_pic = request.POST['profile_pic']
        if first_name and last_name and username and email and study_field and pass1 and pass2 and groups:
            if pass1 == pass2:
                try:
                    user = User.objects.get(email=email)
                    return render(request,'accounts/register.html',
                                  {'error': "That email is already registered. Please login"})
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(username=username)
                        return render(request, 'accounts/register.html',
                                      {'error': "That username is already taken."})
                    except User.DoesNotExist:
                        new_user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=pass1)
                        add_chat_rooms(new_user)
                        create_profile(new_user, study_field,groups,profile_pic)
                        user = auth.authenticate(username= username,password=pass1)
                        auth.login(request, user)
                        return redirect('mainapp:homeView')
            else:
                return render(request, 'accounts/register.html', {'error': "Password do not match"})
        else:
            return render(request, 'accounts/register.html', {'error': "Check missing fields"})
    cohorts = Group.objects.all()
    study_fields = Group.objects.filter(parent_group=0)
    return render(request, 'accounts/register.html',{'cohorts':cohorts,'study_fields':study_fields})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'accounts/login.html',{'error':'Invalid credentials'})
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')


def create_profile(user, study_field, groups, profile_pic):
    if profile_pic:
        new_profile = UserProfile(user=user, profile_photo=profile_pic,study_field=study_field,user_groups=groups)
    else:
        new_profile = UserProfile(user=user, study_field=study_field, user_groups=groups)
    new_profile.save()




