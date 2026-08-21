import os
from celery import Celery
from dotenv import load_dotenv

#celery configurations

load_dotenv() 

CELERY_BROKER_URL=os.getenv("REDIS_URL")

os.environ.setdefault("DJANGO_SETTINGS_MODULE","urlshortener.settings")

app=Celery("urlshortner",broker=CELERY_BROKER_URL)

app.config_from_object("django.conf:settings",namespace="CELERY")

app.autodiscover_tasks()