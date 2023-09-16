import logging
import datetime
import smtplib
from sched import scheduler

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job
from django_apscheduler.models import DjangoJobExecution

import mailing
from client.models import Client
from mailing.models import Mailing, Log

logger = logging.getLogger(__name__)


def my_job():
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

    scheduler.start()
    print("Scheduler started!")


def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      my_job,
      trigger=CronTrigger(second="*/10"),  # Every 10 seconds
      id="my_job",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    logger.info("Added job 'my_job'.")

    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
