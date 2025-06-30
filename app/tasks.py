import os
from celery import Celery
import requests
from bs4 import BeautifulSoup

celery = Celery(
    "scheduled_scraper",
    broker=os.getenv("CELERY_BROKER_URL")
)

@celery.task(name="app.tasks.scrape_and_check")
def scrape_and_check(url, keywords):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=' ', strip=True).lower()

        matched = [kw for kw in keywords if kw.lower() in text]

        return {"url": url, "matched_keywords": matched}
    except Exception as e:
        return {"url": url, "error": str(e)}
