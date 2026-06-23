from celery import Celery
from helpers.config import settings

celery_worker = Celery(
    "financial_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['services.redis.tasks']
)