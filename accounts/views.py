import re

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
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
from django.utils.safestring import mark_safe
from django.http import JsonResponse


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


@csrf_exempt
@anonymous_required
def register_view(request):
    cohorts = Cohort.objects.all()
    study_fields = Cohort.objects.filter(level=0)
    if request.is_ajax():
        data = request.POST
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        study_field = data['study_field']
        pass1 = data['password1']
        pass2 = data['password2']
        school = data['school']
        groups = create_groups_list(data['cohorts'])
        if first_name and last_name and username and email and study_field and pass1 and pass2 and groups and school:
            if not is_valid_email(email):
                response = {"message": "Invalid email address", "code": 1}
                return JsonResponse(response)
            if pass1 == pass2:
                if not email_is_unique(email):
                    response = {'message': "There exists an account associated with that email address."
                                           "Please login or use a different email address", 'code': 1}
                    return JsonResponse(response)

                if not username_is_unique(username):
                    response = {'message': "That username is already taken.", 'code': 1}
                    return JsonResponse(response)
                new_user = User(first_name=first_name, last_name=last_name,
                                email=email, username=username)
                new_user.set_password(pass1)
                new_user.is_active = False
                new_user.save()
                # create user profile
                try:
                    profile_photo = request.FILES['profile_photo']
                    new_profile = create_profile(new_user, study_field, groups, school, profile_photo)
                except MultiValueDictKeyError:
                    # user did not upload profile picture. Use default profile pic
                    print('no file found')
                    new_profile = create_profile(new_user, study_field, groups, school)

                # add channels through which user can chat one-on-one with each member
                add_chat_rooms(new_user)
                increment_group_members(groups)

                # send a confirmation link to the user email
                current_site = get_current_site(request)
                if send_link_via_mail(current_site, email, request.user):
                    response = {'message': 'Success', 'code': 0, 'email': email}
                    return JsonResponse(response)
                else:
                    new_user.delete()
                    response = {'message': 'Something went wrong when validating your email. '
                                           'Please provide valid school email then try'
                                           ' again. If the problem persists, contact our support team ',
                                'code': 1}
                    return JsonResponse(response)
            else:
                response = {'message': 'Password do not match', 'code': 1}
                return JsonResponse(response)
        else:
            response = {'message': "Blank fields detected", "code": 1}
            return JsonResponse(response)

    return render(request, 'accounts/register.html', {'cohorts': cohorts, 'study_fields': study_fields})


@anonymous_required
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username_or_email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('mainapp:homeView')

        else:
            user = User.objects.filter(email=username_or_email).first()
            if user:
                auth_user = authenticate(username=user.username, password=password)
                if auth_user is not None and auth_user.is_active:
                    login(request, auth_user)
                    return redirect('mainapp:homeView')
            return render(request, 'accounts/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


# Create profile for the registered user
def create_profile(user, field_id, groups, school, profile_photo=None):
    study_field = Cohort.objects.get(id=int(field_id))
    if profile_photo is not None:
        handle_uploaded_file(profile_photo, 'profile_photos')
        new_profile = UserProfile(user=user,
                                  profile_photo='profile_photos' + '/' + profile_photo.name,
                                  study_field=study_field, user_groups=groups, school=school
                                  )
    else:
        new_profile = UserProfile(user=user, study_field=study_field, user_groups=groups, school=school)
    new_profile.save()
    return new_profile


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
        return HttpResponse('Activation link is invalid or expired')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('mainapp:homeView')
    return redirect('mainapp:homeView')


# groups to recommend during registration based on the study_field chosen
@csrf_exempt
def get_subcohorts(request):
    if request.is_ajax():
        try:
            coh_id = request.POST['coh_id']
            cohort = Cohort.objects.get(id=coh_id)
        except Cohort.DoesNotExist:
            raise Http404("No cohort matches the given query.")
        subcohorts = cohort.get_descendants(include_self=True)
        cohorts_list = []
        index = 0
        for cohort in subcohorts:
            cohorts_list.append(cohort_to_json(cohort))
        subcohorts = cohorts_list
        return JsonResponse(subcohorts, safe=False)
    else:
        raise Http404("Request is not ajax")


def cohort_to_json(cohort):
    return {
        'id': cohort.id,
        'title': cohort.title,
        'logo': cohort.logo.url,
        'no_of_members': cohort.no_of_members,
        'total_posts': cohort.total_posts,
        'date_created': str(cohort.date_created)
    }


def create_groups_list(user_array):
    groups_list = user_array.split(',')
    groups_list.pop()
    return [int(group_id) for group_id in groups_list]


def increment_group_members(groups):
    for group in groups:
        group = get_object_or_404(Cohort, id=group)
        group.no_of_members += 1
        group.save()


@anonymous_required
def email_confirmation_view(request):
    if request.method == 'POST':
        return render(request, 'accounts/confirm-email.html', {'email': request.POST['email']})
    return redirect('accounts:register')


@csrf_exempt
def resend_activation_link(request):
    if request.is_ajax():
        old_email = request.POST['old-email']
        new_email = request.POST['new-email']
        if old_email and new_email:
            if not is_valid_email(new_email):
                response = {"message": "Invalid email address. Please provide a valid school email", 'code': 1}
                return JsonResponse(response)

            users = User.objects.filter(email=old_email)
            print(users)
            if users.count() == 1:
                user = users.first()
                current_site = get_current_site(request)
                if send_link_via_mail(current_site, new_email, user):
                    if email_is_unique(new_email) or old_email == new_email:
                        user.email = new_email
                        user.save()
                        response = {'message': "Your email address was updated successfully"
                                               " and an activation link was sent sent to " + new_email, 'code': 0}
                        if old_email == new_email:
                            response = {'message': 'New activation link has been sent to: ' + new_email, 'code': 0}
                    else:
                        response = {'message': "There exists another account associated with that email address."
                                               "Please login or use a different email address", 'code': 1}
                else:
                    response = {'message': 'Something went wrong when validating your email. '
                                           'Please provide a valid school email and then try'
                                           ' again. If the problem persists, contact our support team ',
                                'code': 1}
            else:
                response = {'message': 'Something went wrong!', 'code': 1}
            return JsonResponse(response)
    return Http404("Invalid request")


def is_valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True if '.ac' in email or '.edu' in email else False
    return False


def email_is_unique(email):
    try:
        user = User.objects.get(email=email)
        return False
    except User.DoesNotExist:
        return True


def username_is_unique(username):
    try:
        user = User.objects.get(username=username)
        return False
    except User.DoesNotExist:
        return True


def send_link_via_mail(current_site, email, user):
    try:
        email_subject = 'Activate Your Account'
        message = render_to_string('accounts/reg-email-body.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        msg = EmailMessage(email_subject, message, to=[email])
        msg.send()
        return True
    except:
        return False


@csrf_exempt
@login_required
def update_profile(request):
    if request.is_ajax():
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        current_interest_id = request.POST['current_interest']
        current_interest = Cohort.objects.get(id=current_interest_id) if current_interest_id else None
        if first_name and last_name and username:
            if username_is_unique(username) or request.user.username == username:
                basic_info = {'first_name': first_name, 'last_name': last_name, 'username': username}
                profile_info = {'current_interest': current_interest}
                user = request.user
                try:
                    profile = UserProfile.objects.get(user=user)
                    for (key, value) in basic_info.items():
                        setattr(user, key, value)
                    user.save()
                    for (key, value) in profile_info.items():
                        setattr(profile, key, value)
                    profile.save()
                    response = {'code': 0, 'message': 'Successfully Updated'}
                    return JsonResponse(response)
                except:
                    response = {'code': 1, 'message': 'Something went wrong!'}
                    return JsonResponse(response)
            response = {'code': 1, 'message': 'That username is already taken'}
            return JsonResponse(response)
        response = {'code': 1, 'message': 'Failed! Please ensure that all fields contain valid values'}
        return JsonResponse(response)
    print('Bad request')
    return redirect('mainapp:homeView')
