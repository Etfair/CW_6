from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from mailing.views import send_msg


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')

    @scheduler.scheduled_job('interval', hours=1, name='auto_hello')
    def auto_hello():
        send_msg()

    scheduler.start()
