from django.apps import AppConfig
from django.conf import settings


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from mailing import operator
            operator.start()