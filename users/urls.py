from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, generate_new_password, VerifyEmailView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('email-confirmation/', TemplateView.as_view(template_name='users/email_confirmation_sent.html'),
         name='email_confirmation'),
    path('verify/<int:rnd_key>/', VerifyEmailView.as_view(), name='verify_email'),
    path('email-confirmed/', TemplateView.as_view(template_name='users/email_confirmed.html'), name='email_confirmed'),
    path('email-confirmation-failed/', TemplateView.as_view(template_name='users/email_confirmation_failed.html'),
         name='email_confirmation_failed'),
]
