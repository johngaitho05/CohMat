from django.urls import path
from . import views
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('register/to_join', views.get_subcohorts, name='to_join'),
    path('register/email-confirmation', views.email_confirmation_view, name='email-confirmation'),
    path('register/email-confirmation/edit',views.edit_email, name='edit-email'),
    path('logout/', views.logout_view, name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),

]
