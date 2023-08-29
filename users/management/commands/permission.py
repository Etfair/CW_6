from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для наполнения базы группы"""
    def handle(self, *args, **kwargs):

        my_group = Group.objects.create(name='Manager')
        perm = Permission.objects.get(content_type__app_label='client', content_type__model='client', codename='add_client')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='client', content_type__model='client', codename='view_client')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='client', content_type__model='client', codename='delete_client')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='client', content_type__model='client', codename='change_client')
        my_group.permissions.add(perm)

        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='add_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='view_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='delete_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='change_mailing')
        my_group.permissions.add(perm)

        my_group = Group.objects.create(name='new_user')
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='view_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='client', content_type__model='client', codename='view_client')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='mailing', content_type__model='mailing', codename='change_mailing')
        my_group.permissions.add(perm)
        perm = Permission.objects.get(content_type__app_label='client', content_type__model='client', codename='change_client')
        my_group.permissions.add(perm)
