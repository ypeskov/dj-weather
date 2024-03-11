import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djweather.settings")

app = Celery("djweather")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = 5

app.autodiscover_tasks()
