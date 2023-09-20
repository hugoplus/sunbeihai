import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sunbeihai.settings.local')

app = Celery('sunbeihai')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()