import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("technical_task_planx")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_day': {
        'task': 'authapp.tasks.statistics_mail_send_task',
        'schedule':crontab(hour=0, minute=0)
    }
}