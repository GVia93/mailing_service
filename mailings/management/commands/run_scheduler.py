from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from mailings.models import Mailing
from mailings.utils import send_mailing
from django.utils import timezone
import time


def check_mailings():
    print("Проверка рассылок...")
    now = timezone.now()
    for mailing in Mailing.objects.filter(status="created", start_time__lte=now, end_time__gte=now):
        send_mailing(mailing)

    Mailing.objects.filter(status="started", end_time__lte=now).update(status="completed")


class Command(BaseCommand):
    help = "Запускает фоновый планировщик рассылок"

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_job(check_mailings, "interval", seconds=3)
        scheduler.start()

        self.stdout.write("Планировщик запущен. Нажмите Ctrl+C для остановки.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()
