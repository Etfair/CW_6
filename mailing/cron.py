import smtplib
from datetime import datetime

import pytz
from django.conf import settings
from django.core.mail import send_mail

from client.models import Client
from mailing.models import Mailing, Log


def my_scheduled_job():
    mailings = Mailing.objects.filter(mail_status='started')
    tz = pytz.timezone('Europe/Moscow')

    for new_mailing in mailings:
        clients = [client.email for client in Client.objects.filter(user=new_mailing.user)]
        if new_mailing.mailing_datetime >= datetime.now(tz):
            mail_subject = new_mailing.message.body_mail if new_mailing.message is not None else 'Тест 1'
            message = new_mailing.message.name_mail if new_mailing.message is not None else 'Тест 2'
            try:
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Успешно', answer='200')
                log.save()
            except smtplib.SMTPException as err:
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', answer=err)
                log.save()
            new_mailing.status = 'done'
            new_mailing.save()
