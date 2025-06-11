from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from applications.constants import StatusChoices
from applications.models import Application
from .models import Notification


@shared_task(name='notifications.tasks.clear_seen_notifications')
def clear_seen_notifications():
    week_ago = timezone.now() - timedelta(weeks=1)
    Notification.objects.filter(is_seen=True, created_at__lte=week_ago).delete()
    return True

@shared_task(name='create_notification')
def create_notification_task(application_id, status, comment=None):
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        return
    receiver = application.owner
    Notification.objects.create(receiver=receiver,
                                content=comment,
                                type=status,
                                application=application)
    if not comment:
        comment = 'Заявка получила новый статус'

    if receiver.email:
        send_mail(
            subject=f'Новое уведомление по заявке № {application_id}',
            message=f'Комментарий: {comment}\nСтатус: {status}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiver.email],
            fail_silently=False,
        )

@shared_task(name='create_notification_for_assignee')
def create_notification_for_assignee_task(application_id, is_revisioned):
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        return
    if not is_revisioned:
        message = f'За вами закреплена заявка № {application_id}.'
        subject = 'Новая заявка'
    else:
        message = f'Заявка № {application_id} доработана студентом.'
        subject = f'Заявка № {application_id}'
    receiver = application.assignee
    Notification.objects.create(receiver=receiver,
                                application=application,
                                type=StatusChoices.FOR_ADMINS,
                                content=message,)
    if receiver.email:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiver.email],
            fail_silently=False,
        )