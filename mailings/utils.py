from django.core.mail import send_mail
from django.conf import settings
from .models import Attempt


def send_mailing(mailing):
    """Отправляет сообщения всем клиентам рассылки и фиксирует попытки."""

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False

            )
            Attempt.objects.create(
                mailing=mailing,
                status='success',
                server_response='Письмо успешно отправлено'
            )
        except Exception as e:
            Attempt.objects.create(
                mailing=mailing,
                status='failed',
                server_response=str(e)
            )
