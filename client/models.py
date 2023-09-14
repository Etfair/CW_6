from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """Клиент рассылки"""
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)
    email = models.EmailField(verbose_name='почта', unique=True)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE, **NULLABLE)
    is_active = models.BooleanField(default=True, **NULLABLE)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic} ({self.email}) ({self.comment}).'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
