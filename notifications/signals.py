from django.db.models.signals import pre_save
from applications.models import Application
from django.dispatch import receiver
from .tasks import create_notification_task

@receiver(pre_save, sender=Application)
def create_notification_signal(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Application.objects.get(pk=instance.pk)
    except Application.DoesNotExist:
        return
    status_changed = old_instance.status != instance.status
    comment_changed = old_instance.comment != instance.comment

    if status_changed or comment_changed:
        comment = instance.comment if comment_changed else None

        create_notification_task.delay(
            application_id=instance.id,
            comment=comment,
            status=instance.status,
        )