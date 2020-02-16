from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

from chat.views import add_chat_rooms
from .models import *
from mainapp.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required
def register_view(request):
    cohorts = Cohort.objects.all()
    study_fields = Cohort.objects.filter(parent_group=0)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        study_field = request.POST['study_field']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        groups = request.POST.getlist('to_join')
        if first_name and last_name and username and email and study_field and pass1 and pass2 and groups:
            if pass1 == pass2:
                try:
                    User.objects.get(email=email)
                    return render(request, 'accounts/register.html',
                                  {'error_message': "That email is already registered. Please login",
                                   'cohorts': cohorts, 'study_fields': study_fields})
                except User.DoesNotExist:
                    try:
                        User.objects.get(username=username)
                        return render(request, 'accounts/register.html',
                                      {'error_message': "That username is already taken.",
                                       'cohorts': cohorts, 'study_fields': study_fields})
                    except User.DoesNotExist:
                        new_user = User(first_name=first_name, last_name=last_name,
                                        email=email, username=username)
                        new_user.set_password(pass1)
                        new_user.is_active = False
                        new_user.save()
                        # add channels through which user can chat one-on-one with each member
                        add_chat_rooms(new_user)
                        try :
                            profile_photo = request.FILES['profile_photo']
                            create_profile(new_user, study_field, groups, profile_photo)
                        except MultiValueDictKeyError:
                            create_profile(new_user, study_field, groups)
                        current_site = get_current_site(request)
                        email_subject = 'Activate Your Account'
                        message = render_to_string('accounts/acc_active_email.html', {
                            'user': new_user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                            'token': account_activation_token.make_token(new_user),
                        })
                        to_email = email
                        email = EmailMessage(email_subject, message, to=[to_email])
                        email.send()
                        return HttpResponse(
                            'We have sent you an email, please confirm your email address to complete registration')
            else:
                return render(request, 'accounts/register.html',
                              {'error_message': "Password do not match",
                               'cohorts': cohorts, 'study_fields': study_fields})
        else:
            return render(request, 'accounts/register.html',
                          {'error_message': "Check missing fields",
                           'cohorts': cohorts, 'study_fields': study_fields})

    return render(request, 'accounts/register.html', {'cohorts': cohorts, 'study_fields': study_fields})


@anonymous_required
def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            login(request, user)
            return redirect('mainapp:homeView')
        else:
            return render(request, 'accounts/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


# Create profile for the registered user
def create_profile(user, study_field, groups, profile_photo=None):
    if profile_photo is not None:
        handle_uploaded_file(profile_photo, 'profile_photos')
        new_profile = UserProfile(user=user, profile_photo='profile_photos'
                                                           + '/' + profile_photo.name, study_field=study_field,
                                                           user_groups=groups
                                  )
    else:
        new_profile = UserProfile(user=user, study_field=study_field, user_groups=groups)
    new_profile.save()


# saving the uploaded profile picture
def handle_uploaded_file(file, desired_location):
    with open(settings.MEDIA_ROOT + '/' + desired_location + '/' + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


# activating account after email confirmation
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('mainapp:homeView')
    else:
        return HttpResponse('Activation link is invalid!')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('mainapp:homeView')


