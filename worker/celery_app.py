from celery import Celery

from backend.app.core.config import settings


celery_app = Celery(
    "supportflow",
    broker=(
        settings.celery_broker_url
    ),
    backend=(
        settings.celery_result_backend
    ),
)


celery_app.conf.update(

    task_serializer="json",

    result_serializer="json",

    accept_content=["json"],

    timezone="UTC",

    enable_utc=True,

    task_track_started=True,

    task_acks_late=True,

    worker_prefetch_multiplier=1,

    broker_transport_options={
        "visibility_timeout": 3600,
    },
)


celery_app.autodiscover_tasks(
    ["worker"]
)