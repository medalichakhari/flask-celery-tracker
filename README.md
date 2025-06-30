# Scheduled Web Scraper & Notifier API

A Flask-based backend project that allows users to track specific **keywords** on web pages. It scrapes URLs at scheduled intervals using **Celery + RabbitMQ**, and sends notifications when matches are found.

---

## Tech Stack

- **Flask** – RESTful API backend
- **Celery** – Background task queue
- **RabbitMQ** – Message broker
- **Redis** - Backend for results
- **BeautifulSoup** – HTML parsing & scraping
- **Docker + Docker Compose** – Containerized environment

---

## Analogy

- `Flask` = Waiter taking your order

- `Celery` = Chef cooking it

- `RabbitMQ` = Order ticket system

- `Redis` = Pickup counter where you check if your meal is ready

## Features

- `POST /track`: Submit a URL and keywords to monitor
- Scrapes the page content periodically
- Matches keywords using text search or regex
- `GET /track-status/<id>`: Check if any matches were found
- Sends alerts via email

---

## Project Structure

```
scheduled_scraper/
│
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # API endpoints
│   ├── tasks.py             # Celery tasks
│   ├── scraper.py           # Scraping logic
│   ├── notifier.py          # Notifications
│   └── config.py            # App/Celery config
│
├── run.py                   # Flask entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```
