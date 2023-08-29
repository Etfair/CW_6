from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    """Пользователь"""
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)

    is_active = models.BooleanField(default=False)
    rnd_key = models.IntegerField(default=0, verbose_name='ключ для верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def add_mailing_group(self):
        mailing_group = Group.objects.get(name='manager')
        if self.groups.filter(id=mailing_group.id).exists():
            self.groups.add(mailing_group)
