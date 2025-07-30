from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт группу 'Менеджеры' и добавляет пользователей с is_manager=True"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        permissions = Permission.objects.filter(
            codename__in=[
                "can_view_all_clients",
                "can_view_all_mailings",
                "can_view_user_list",
                "can_block_users",
                "can_toggle_mailing",
            ]
        )

        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' создана."))
