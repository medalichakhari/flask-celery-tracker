import os
import re
from celery import Celery
import requests
from bs4 import BeautifulSoup

celery = Celery(
    "scheduled_scraper",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

@celery.task(name="app.tasks.scrape_and_check")
def scrape_and_check(url, keywords):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.get_text(separator=' ', strip=True)

        results = []
        for kw in keywords:
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            matches = pattern.findall(text)

            snippets = []
            sentences = re.split(r'(?<=[.!?]) +', text)
            for sentence in sentences:
                if pattern.search(sentence):
                    snippet = sentence.strip()
                    if snippet not in snippets:
                        snippets.append(snippet)
                    if len(snippets) >= 3:
                        break

            results.append({
                "keyword": kw,
                "count": len(matches),
                "snippets": snippets
            })

        return {
            "url": url,
            "matches": results
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

