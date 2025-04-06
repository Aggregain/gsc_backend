import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsc_backend.settings')

app = Celery('gsc_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'delete_expired_otp_codes': {
#         'task': 'customers.tasks.delete_expired_otp_codes',
#         'schedule': crontab(hour='8', minute='0'),
#     }
# }
#
# app.conf.beat_schedule = {
#     'check_menu_for_updates': {
#         'task': 'iiko.tasks.check_menu_for_updates',
#     'schedule': crontab(hour='8', minute='0'),
#     }
# }
