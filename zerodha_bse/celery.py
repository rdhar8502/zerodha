from __future__ import absolute_import, unicode_literals

from celery import Celery
from datetime import datetime, timedelta

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zerodha_bse.settings')

app = Celery('zerodha_bse')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'app.utils.set_data',
        'schedule': 1.0,
    }
}

app.conf.timezone = 'UTC'

app.autodiscover_tasks()
