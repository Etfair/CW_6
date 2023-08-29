from random import randint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from config import settings
from users.forms import UserRegistrForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrForm
    success_url = reverse_lazy('users:email_confirmation')

    def form_valid(self, form):
        user = form.save()
        user.rnd_key = randint(1, 2147483644)
        user.save()
        user = form.save(commit=False)
        user.save()
        if form.is_valid():
            my_group = Group.objects.get(name='manager')
            my_group.user_set.add(user)

        verify_url = reverse('users:verify_email', args=[user.rnd_key])
        verify_link = self.request.build_absolute_uri(verify_url)
        send_mail(
            subject='Подтвердите свой электронный адрес',
            message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: {verify_link}',
            from_email='Unfearble@yandex.ru',
            recipient_list=[user.email, ],
            fail_silently=False
        )
        return super().form_valid(form)


class VerifyEmailView(View):
    def get(self, request, rnd_key):
        try:
            user = User.objects.get(rnd_key=rnd_key)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('users:email_confirmed'))
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('users:email_confirmation_failed'))


class EmailConfirmationView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_new_password(request):
    new_password = ''.join([str(randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('mail'))

