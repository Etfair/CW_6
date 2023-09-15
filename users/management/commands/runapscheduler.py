import logging
import datetime
import smtplib
import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

import mailing
from client.models import Client
from mailing.models import Mailing, Log

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs apscheduler."
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @register_job(scheduler, "cron", hour=1, replace_existing=True)
    def handle(*args, **options):
        # mailings = Mailing.objects.filter(mail_status='created')
        mailings = Mailing.objects.all()
        tz = pytz.timezone('Europe/Moscow')
        print(3)
        for new_mailing in mailings:
            clients = [client.email for client in Client.objects.filter(user=new_mailing.user)]
            print(2)
            if new_mailing.mailing_datetime <= datetime.datetime.now(tz):
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
                new_mailing.mail_status = 'done'
                new_mailing.save()


    scheduler.start()
    print("Scheduler started!")
