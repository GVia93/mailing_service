from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from .models import Attempt


def send_mailing(mailing):
    """Отправляет сообщения всем клиентам рассылки и фиксирует попытки."""

    if mailing.status != "started":
        mailing.status = "started"
        mailing.save(update_fields=["status"])

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            Attempt.objects.create(
                mailing=mailing,
                owner=mailing.owner,
                status="success",
                server_response="Письмо успешно отправлено",
            )
        except Exception as e:
            Attempt.objects.create(
                mailing=mailing,
                owner=mailing.owner,
                status="failed",
                server_response=str(e),
            )

    if mailing.end_time <= now():
        mailing.status = "completed"
        mailing.save(update_fields=["status"])
