import os
import threading

from django.apps import AppConfig


class ShortenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shortener'

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":
            return
        if os.environ.get("CELERY_WORKER_STARTED"):
            return
        os.environ["CELERY_WORKER_STARTED"] = "true"

        from urlshortener.celery_client import app as celery_app

        def start_worker():
            celery_app.worker_main(
                argv=["worker", "--loglevel=info", "--pool=solo"]
            )

        threading.Thread(target=start_worker, daemon=True).start()