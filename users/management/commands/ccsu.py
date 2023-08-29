from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда создания суперюзера"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='and90dmb@mail.ru',
            first_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('123456')
        user.save()
