from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Mail(models.Model):
    """Сообщение"""
    name_mail = models.CharField(max_length=50, verbose_name='тема письма')
    body_mail = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.name_mail}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письмо'


class Mailing(models.Model):
    """Рассылка"""
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    )

    mailing_datetime = models.DateTimeField(verbose_name='Время', default=timezone.now)
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Периодичность')
    mail_status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED)
    message = models.ForeignKey('Mail', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Рассылка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return f"{self.mail_status}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    date_attempt = models.DateTimeField(verbose_name='Дата попытки')
    status = models.CharField(max_length=150, verbose_name='Статус попытки')
    answer = models.TextField(**NULLABLE, verbose_name='ответ сервера')
    mailing = models.ForeignKey('Mailing', **NULLABLE, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status} {self.date_attempt}"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
