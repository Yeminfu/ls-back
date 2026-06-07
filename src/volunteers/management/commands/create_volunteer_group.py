# management/commands/create_volunteer_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создает группу Волонтеры'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='volunteers')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Волонтеры" создана'))
        else:
            self.stdout.write('Группа "Волонтеры" уже существует')