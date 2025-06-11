import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsc_backend.settings')

app = Celery('gsc_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_seen_notifications': {
        'task': 'notifications.tasks.clear_seen_notifications',
        'schedule': crontab(hour='8', minute='0'),
    }
}

