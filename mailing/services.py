from django.conf import settings
from django.core.cache import cache

from mailing.models import Mailing, Mail


def get_cache_mailing():
    if settings.CACHE_ENABLED:
        key = f'log_list'
        log_list = cache.get(key)
        if log_list is None:
            log_list = Mailing.object.log_set.all()
            cache.set(key, log_list)
    else:
        log_list = Mailing.object.log_set.all()

    return log_list


def get_cache_mail_detail():
    if settings.CACHE_ENABLED:
        key = f'mail_list'
        mail_list = cache.get(key)
        if mail_list is None:
            mail_list = Mail.objects.all()
            cache.set(key, mail_list)
    else:
        mail_list = Mail.objects.all()

    return mail_list
