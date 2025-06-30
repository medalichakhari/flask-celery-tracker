from celery import Celery
import os

celery = Celery(
    "scheduled_scraper",
    broker=os.environ.get("CELERY_BROKER_URL")
)

@celery.task
def test_task():
    print("Celery is working!")
    return "Success"
