from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from applications.models import Application
from .models import Notification


@shared_task(name='create_notification')
def create_notification_task(application_id, status, comment=None):
    if not comment:
        comment = 'Заявка получила новый статус'
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        return
    receiver = application.owner
    Notification.objects.create(receiver=receiver,
                               content=comment,
                               type=status,
                               application=application)

    if receiver.email:
        send_mail(
            subject='Новое уведомление по заявке',
            message=f'Комментарий: {comment}\nСтатус: {status}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiver.email],
            fail_silently=False,
        )
