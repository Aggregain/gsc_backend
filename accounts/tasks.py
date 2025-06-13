
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail



@shared_task(name='send_confirmation_email_task')
def send_confirmation_email(confirmation_url, email):
    send_mail(
            'Подтверждение регистрации',
            f'Спасибо за регистрацию! Для подтверждения вашего email перейдите по ссылке: {confirmation_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

@shared_task(name='send_password_reset_task')
def send_password_reset_email(reset_url, email):
    send_mail(
        'Сброс пароля',
        f'Для сброса пароля перейдите по ссылке: {reset_url}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )