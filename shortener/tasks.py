from celery import shared_task
from .models import URL
from .redis_client import redis_client



@shared_task
def update_analytics(short_code,accessed_at):               # this the task from /redirect endpoint that will be executed in background
    url=URL.objects.get(short_code=short_code)

    url.click_count+=1
    url.last_accessed=accessed_at

    url.save()

    #invalidates if the stats data is cached
    redis_client.delete(f"url:{short_code}:stats")