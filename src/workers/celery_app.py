from celery import Celery
import os

celery_app = Celery(
    "rag_worker",
    broker=os.getenv("CELERY_BROKER_URL"),
)


celery_app.conf.update(
    task_serialize="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
