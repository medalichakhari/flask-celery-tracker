import os
import re

import requests
from bs4 import BeautifulSoup
from celery import Celery

from app.utils import send_email

celery = Celery(
    "scheduled_scraper",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery.conf.beat_schedule = {}
celery.conf.timezone = "UTC"


@celery.task(name="app.tasks.scrape_and_check")
def scrape_and_check(url, keywords):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.get_text(separator=" ", strip=True)

        results = []
        email_matches = []
        for kw in keywords:
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            matches = pattern.findall(text)

            snippets = []
            sentences = re.split(r"(?<=[.!?]) +", text)
            for sentence in sentences:
                if pattern.search(sentence):
                    snippet = sentence.strip()
                    if snippet not in snippets:
                        snippets.append(snippet)
                    if len(snippets) >= 3:
                        break

            result = {"keyword": kw, "count": len(matches), "snippets": snippets}
            results.append(result)

            if matches:
                email_matches.append(result)

        if email_matches:
            subject = f"Keyword(s) found in: {url}"
            body = "Summary of matches:\n\n"
            for m in email_matches:
                body += f"Keyword: {m['keyword']}\n"
                body += f"Count: {m['count']}\n"
                body += (
                    "Snippets:\n" + "\n".join(f"- {s}" for s in m["snippets"]) + "\n\n"
                )
            send_email(subject, body)

        return {"url": url, "matches": results}
    except Exception as e:
        return {"url": url, "error": str(e)}
