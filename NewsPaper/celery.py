import os
from celery import Celery, schedules
# from news.tasks import send_task
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'new_post_every_week': {
        'task': 'news.tasks.week_notify',
        'schedule': crontab(minute='0', hour='8', day_of_week='monday'),

    }

}

app.autodiscover_tasks()
