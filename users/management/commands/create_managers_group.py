from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт группу 'Менеджеры' и добавляет пользователей с is_manager=True"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        self.stdout.write(
            self.style.SUCCESS(
                f"Группа 'Менеджеры' {'создана' if created else 'уже существует'}."
            )
        )
