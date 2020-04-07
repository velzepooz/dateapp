import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dateapp.settings')

app = Celery('dateapp')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-report-every-month-email': {
        'task': 'cards.tasks.send_month_report_email',
        'schedule': crontab(minute=0, hour=9, day_of_month=1),  # every month at 9-00
    },
    'send-report-every-week-email': {
        'task': 'cards.tasks.send_week_report_email',
        'schedule': crontab(minute=0, hour=9, day_of_week='monday'),  # every week at 9-00
    },
    'send-report-every-day-email': {
        'task': 'cards.tasks.send_day_report_email',
        'schedule': crontab(minute=0, hour=9),  # every day at 9-00
    },
    'send-report-every-month-tg': {
        'task': 'bot.tasks.send_month_report_tg',
        'schedule': crontab(minute=0, hour=9, day_of_month=1),  # every month at 9-00
    },
    'send-report-every-week-tg': {
        'task': 'bot.tasks.send_week_report_tg',
        'schedule': crontab(minute=0, hour=9, day_of_week='monday'),  # every week at 9-00
    },
    'send-report-every-day-tg': {
        'task': 'bot.tasks.send_day_report_tg',
        'schedule': crontab(minute=0, hour=9),  # every day at 9-00
    },
}
