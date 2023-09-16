import datetime
import smtplib

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

import mailing
from client.models import Client
from mailing.models import Mailing, Log


class Command(BaseCommand):

    def handle(*args, **options):
        tz = pytz.timezone('Europe/Moscow')
        for mailing in Mailing.objects.all():
        # for mailing in Mailing.objects.filter(mail_status='created'):
            print(3)
            for client in mailing.client.all():
                log = Log.objects.filter(client=client.pk, mailing=mailing.pk)
                print(2)

                if mailing.mailing_datetime <= datetime.datetime.now(tz):
                    mail_subject = mailing.message.body_mail
                    message = mailing.message.name_mail
                    print(1)
                    try:
                        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [client.email])
                        log = Log.objects.create(date_attempt=datetime.datetime.now(tz), status='Успешно', answer='200')
                        log.save()
                    except smtplib.SMTPException as err:
                        log = Log.objects.create(date_attempt=datetime.datetime.now(tz), status='Ошибка', answer=err)
                        log.save()
                    mailing.mail_status = 'done'
                    mailing.save()
