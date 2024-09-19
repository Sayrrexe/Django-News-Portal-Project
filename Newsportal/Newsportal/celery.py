import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Newsportal.settings')
app = Celery('Newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    # Настройки расписания на еженедельную рассылку новостей
    'weekly_notification': {
        'task': 'news.tasks.weekly_notification',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}