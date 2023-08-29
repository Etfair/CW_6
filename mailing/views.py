import smtplib
from datetime import datetime
import pytz
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from blog.models import Blog
from client.models import Client
from mailing.forms import MailForm, MailingForms
from mailing.models import Mail, Mailing, Log
from mailing.services import get_cache_mailing, get_cache_mail_detail


class MailCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.add_mail'

    def get_success_url(self):
        return reverse('view_mail', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.change_mail'

    def get_success_url(self):
        return reverse('view_mail', args=[self.object.pk])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailListView(ListView):
    model = Mail
    template_name = 'mailing/mail_list.html'
    permission_required = 'mailing.view_mail'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(*args, **kwargs)


class MailDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mail
    template_name = 'mailing/mail_detail.html'
    permission_required = 'mailing.view_mail'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        get_cache_mail_detail()

        return context_data


class MailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mail
    permission_required = 'mailing.delete_mail'

    def get_success_url(self):
        return reverse('mail')


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        get_cache_mailing()

        return context_data


def main(request):
    clients = len(Client.objects.all().distinct('email'))
    blog = Blog.objects.filter(is_published=True).order_by('?')
    mailing = len(Mailing.objects.all())
    mailing_active = len(Mailing.objects.filter(mail_status='started'))
    context = {
        'title': "Главная",
        'blog': blog[:3],
        'mailing': mailing,
        'mailing_active': mailing_active,
        'clients': clients
    }
    return render(request, 'mailing/main_list.html', context)


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForms
    permission_required = 'mailing.add_mailing'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        tz = pytz.timezone('Europe/Moscow')
        clients = [client.email for client in Client.objects.filter(user=self.request.user)]
        new_mailing = form.save()

        if new_mailing.mailing_datetime <= datetime.now(tz):
            mail_subject = new_mailing.message.body_mail if new_mailing.message is not None else 'Рассылка'
            message = new_mailing.message.name_mail if new_mailing.message is not None else 'Рассылка'
            try:
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Успешно', answer='200', mailing=new_mailing)
                log.save()
            except smtplib.SMTPDataError as err:
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', answer=err, mailing=new_mailing)
                log.save()
            except smtplib.SMTPException as err:
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', answer=err, mailing=new_mailing)
                log.save()
            except Exception as err:
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', answer=err, mailing=new_mailing)
                log.save()
            new_mailing.status = 'done'
            if new_mailing.user is None:
                new_mailing.user = self.request.user
            new_mailing.save()

        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(*args, **kwargs)


def send_msg():
    mailings = Mailing.objects.filter(mail_status='created')
    tz = pytz.timezone('Europe/Moscow')
    print(3)
    for new_mailing in mailings:
        clients = [client.email for client in Client.objects.filter(user=new_mailing.user)]
        print(2)
        if new_mailing.mailing_datetime >= datetime.datetime.now(tz):
            mail_subject = new_mailing.message.body_mail if new_mailing.message is not None else 'Тест 1'
            message = new_mailing.message.name_mail if new_mailing.message is not None else 'Тест 2'
            print(1)
            try:
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
                log = Log.objects.create(date_attempt=datetime.datetime.now(tz), status='Успешно', answer='200')
                log.save()
            except smtplib.SMTPException as err:
                log = Log.objects.create(date_attempt=datetime.datetime.now(tz), status='Ошибка', answer=err)
                log.save()
            new_mailing.status = 'done'
            new_mailing.save()
