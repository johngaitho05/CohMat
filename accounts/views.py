import random
import re

from django.db.models import Count
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from projectdir.utils import randomColor
from .models import *
from mainapp.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
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


@csrf_exempt
@anonymous_required
def register_view(request):
    cohorts = Cohort.objects.all()
    study_fields = Cohort.objects.filter(level=0).order_by('title')
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
        Idslist = (data['cohorts'])
        if first_name and last_name and username and email and study_field and pass1 and pass2 and school:
            print(study_field)
            defaultGroup = [Cohort.objects.get(id=int(study_field))]
            cohorts = getCohorts(Idslist) + defaultGroup if Idslist else defaultGroup
            if not is_valid_email(email):
                response = {"message": "Invalid email address.Please provide a valid school email", "code": 1}
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
                    create_profile(new_user, study_field, school, cohorts, profile_photo)
                except MultiValueDictKeyError:
                    # user did not upload profile picture. Use default profile pic
                    create_profile(new_user, study_field, school, cohorts)
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
            response = {'message': "Blank fields detected. Please fill up all the required fields", "code": 1}
            return JsonResponse(response)

    return render(request, 'accounts/register.html', {'cohorts': cohorts, 'study_fields': study_fields})


@anonymous_required
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            user = User.objects.filter(email=username_or_email).first()
        if user:
            if not user.is_active:
                return render(request, 'accounts/confirm-email.html', {'email': user.email})
            user = authenticate(username=username_or_email, password=password)
            if user:
                auth_user = authenticate(username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    return redirect('mainapp:homeView')
        return render(request, 'accounts/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


# Create profile for the registered user
def create_profile(user, field_id, school, cohorts, profile_photo=None):
    study_field = Cohort.objects.get(id=int(field_id))
    if profile_photo is not None:
        handle_uploaded_file(profile_photo, 'profile_photos')
        new_profile = UserProfile(user=user, profile_photo='profile_photos' + '/' +
                                                           profile_photo.name, study_field=study_field, school=school
                                  )
    else:
        new_profile = UserProfile(user=user, study_field=study_field, school=school)
    new_profile.save()
    for cohort in cohorts:
        new_profile.user_cohorts.add(cohort)
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
        subCohorts = cohort.get_descendants(include_self=False) \
            .annotate(number_of_members=Count('user_cohorts'), total_posts=Count('question')).order_by('level')
        subCohorts = [cohort_to_json(cohort) for cohort in subCohorts]
        return JsonResponse(subCohorts, safe=False)
    return redirect('accounts:register')


def cohort_to_json(cohort):
    color1 = randomColor()
    color2 = randomColor()
    return {
        'id': cohort.id,
        'title': cohort.title,
        'logo': cohort.logo.url if cohort.logo else None,
        'background_color': 'linear-gradient(to top,' + color1 + ' 0%,' + color2 + ' 100%)',
        'no_of_members': cohort.number_of_members,
        'total_posts': cohort.total_posts,
        'date_created': str(cohort.date_created)
    }


def getCohorts(IdsList):
    groups_list = IdsList.split(',')
    groups_list.pop()
    refined_list = list(map(int, groups_list))
    cohorts = [getCohort(coh_id) for coh_id in refined_list]
    return [cohort for cohort in cohorts if cohort]


def getCohort(coh_id):
    try:
        cohort = Cohort.objects.get(id=coh_id)
        return cohort
    except Cohort.DoesNotExist:
        return None


@anonymous_required
def email_confirmation_view(request):
    if request.method == 'POST':
        return render(request, 'accounts/confirm-email.html', {'email': request.POST['email'], 'first': True})
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
    raise Http404("Something went wrong")


@csrf_exempt
@login_required
def update_profile(request):
    if request.is_ajax() or request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        new_interest_id = request.POST['new-interest']
        current_interest = Cohort.objects.get(id=new_interest_id) if new_interest_id else None
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
            else:
                response = {'code': 1, 'message': 'That username is already taken'}
        else:
            response = {'code': 1, 'message': 'Failed! Please ensure that all fields contain valid values'}
        if request.is_ajax():
            return JsonResponse(response)
        return render(request, 'mainapp/profile.html', {'message': response})
    return redirect('mainapp:homeView')


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
