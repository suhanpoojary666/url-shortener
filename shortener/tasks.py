from celery import shared_task
from .models import URL


@shared_task
def update_analytics(url_id,accessed_at):               # this the task from /redirect endpoint that will be executed in background
    url=URL.objects.get(id=url_id)

    url.click_count+=1
    url.last_accessed=accessed_at

    url.save()