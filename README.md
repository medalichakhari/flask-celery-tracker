# 🕷️ Flask-Celery Web Scraping Tracker

A powerful Flask-based API that allows you to track specific keywords on web pages with automated scheduling and email notifications. Built with Celery for background processing and containerized with Docker for easy deployment.

## ✨ Features

- **🎯 One-time Tracking**: Submit a URL and keywords for immediate scraping
- **⏰ Scheduled Monitoring**: Set up recurring scraping jobs at custom intervals
- **📧 Email Notifications**: Get alerts when keywords are found on pages
- **📊 Real-time Status**: Check task progress and results via API
- **🎨 Context Snippets**: Receive relevant text snippets where keywords were found
- **🐳 Containerized**: Full Docker Compose setup for easy deployment
- **📈 Monitoring**: Built-in Flower dashboard for Celery task monitoring

## 🛠️ Tech Stack

- **Flask** – RESTful API backend
- **Celery** – Background task queue with beat scheduler
- **RabbitMQ** – Message broker
- **Redis** – Results backend
- **BeautifulSoup4** – HTML parsing & scraping
- **Marshmallow** – Request validation and serialization
- **Docker + Docker Compose** – Containerized environment
- **Flower** – Celery monitoring dashboard

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Client   │───▶│   Flask     │───▶│  RabbitMQ   │
│   Request   │    │    API      │    │   Broker    │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Redis    │◀───│   Celery    │◀───│   Celery    │
│   Results   │    │   Worker    │    │    Beat     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐    ┌─────────────┐
│   Flower    │    │    Email    │
│  Dashboard  │    │  Notifier   │
└─────────────┘    └─────────────┘
```

## 📁 Project Structure

```
flask-celery-tracker/
│
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # API endpoints
│   ├── tasks.py             # Celery tasks & configuration
│   ├── schemas.py           # Request validation schemas
│   ├── utils.py             # Email utilities
│   ├── config.py            # Application configuration
│   └── db.py                # Database utilities
│
├── run.py                   # Flask application entry point
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd flask-celery-tracker
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development

# Celery Configuration
CELERY_BROKER_URL=pyamqp://guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
NOTIFY_EMAIL=notifications@example.com
```

### 3. Launch with Docker Compose

```bash
docker-compose up -d
```

This will start all services:

- **Flask API**: http://localhost:5000
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **Flower Dashboard**: http://localhost:5555
- **Redis**: localhost:6379

### 4. Verify Installation

```bash
curl http://localhost:5000/status/test
```

## 📚 API Documentation

### Base URL

```
http://localhost:5000
```

### Endpoints

#### 1. One-time Keyword Tracking

**POST** `/track`

Track keywords on a URL immediately.

```bash
curl -X POST http://localhost:5000/track \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "keywords": ["python", "flask", "celery"]
  }'
```

**Response:**

```json
{
  "task_id": "abc123-def456-ghi789"
}
```

#### 2. Schedule Recurring Tracking

**POST** `/track/schedule`

Set up recurring keyword monitoring.

```bash
curl -X POST http://localhost:5000/track/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com",
    "keywords": ["AI", "machine learning", "GPT"],
    "interval_minutes": 30
  }'
```

**Response:**

```json
{
  "message": "Scheduled scraping every 30 minutes.",
  "job_name": "scrape-a1b2c3d4e5f6"
}
```

#### 3. Check Task Status

**GET** `/status/<task_id>`

Check the status and results of a tracking task.

```bash
curl http://localhost:5000/status/abc123-def456-ghi789
```

**Response (In Progress):**

```json
{
  "status": "in progress"
}
```

**Response (Completed):**

```json
{
  "status": "completed",
  "result": {
    "url": "https://example.com",
    "matches": [
      {
        "keyword": "python",
        "count": 5,
        "snippets": [
          "Python is a versatile programming language...",
          "Learn Python for data science and web development...",
          "Python frameworks like Flask and Django..."
        ]
      }
    ]
  }
}
```

**Response (Failed):**

```json
{
  "status": "failed",
  "error": "Connection timeout"
}
```

### Request Schema

#### TrackRequest

```json
{
  "url": "string (required, valid URL)",
  "keywords": ["array of strings (required)"]
}
```

#### ScheduleRequest

```json
{
  "url": "string (required, valid URL)",
  "keywords": ["array of strings (required)"],
  "interval_minutes": "integer (optional, default: 60, min: 1)"
}
```

## 🔧 Development

### Running Locally (without Docker)

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Start Redis and RabbitMQ:**

```bash
# Using Docker for services only
docker run -d -p 6379:6379 redis:7
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

3. **Set environment variables:**

```bash
export CELERY_BROKER_URL=pyamqp://guest@localhost:5672//
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

4. **Start services:**

```bash
# Terminal 1: Flask API
python run.py

# Terminal 2: Celery Worker
celery -A app.tasks.celery worker --loglevel=info

# Terminal 3: Celery Beat (for scheduled tasks)
celery -A app.tasks.celery beat --loglevel=info

# Terminal 4: Flower (optional monitoring)
celery -A app.tasks.celery flower
```

### Testing

```bash
# Test one-time tracking
curl -X POST http://localhost:5000/track \
  -H "Content-Type: application/json" \
  -d '{"url": "https://httpbin.org/html", "keywords": ["Herman"]}'

# Test scheduling
curl -X POST http://localhost:5000/track/schedule \
  -H "Content-Type: application/json" \
  -d '{"url": "https://httpbin.org/html", "keywords": ["Melville"], "interval_minutes": 1}'
```

## 📊 Monitoring

### Flower Dashboard

Access the Celery monitoring dashboard at http://localhost:5555

Features:

- Real-time task monitoring
- Worker status and statistics
- Task history and results
- Broker monitoring

### RabbitMQ Management

Access the RabbitMQ management interface at http://localhost:15672

- Username: `guest`
- Password: `guest`

## ⚙️ Configuration

### Environment Variables

| Variable                | Description                   | Default                          |
| ----------------------- | ----------------------------- | -------------------------------- |
| `FLASK_APP`             | Flask application entry point | `run.py`                         |
| `FLASK_ENV`             | Flask environment             | `development`                    |
| `CELERY_BROKER_URL`     | Message broker URL            | `pyamqp://guest@rabbitmq:5672//` |
| `CELERY_RESULT_BACKEND` | Results backend URL           | `redis://redis:6379/0`           |
| `SMTP_SERVER`           | SMTP server for emails        | `smtp.example.com`               |
| `SMTP_PORT`             | SMTP port                     | `587`                            |
| `SMTP_USERNAME`         | SMTP username                 | `noreply@example.com`            |
| `SMTP_PASSWORD`         | SMTP password                 | `changeme123`                    |
| `NOTIFY_EMAIL`          | Notification recipient        | `admin@example.com`              |

### Email Setup

To enable email notifications:

1. **Gmail Setup:**

   - Enable 2-factor authentication
   - Generate an app password
   - Use `smtp.gmail.com:587`

2. **Other Providers:**
   - Update SMTP settings in `.env`
   - Ensure STARTTLS is supported

## 📝 How It Works

1. **Request Submission**: Client submits URL and keywords via API
2. **Task Queuing**: Flask queues a Celery task with the scraping job
3. **Background Processing**: Celery worker fetches and parses the webpage
4. **Keyword Matching**: BeautifulSoup extracts text and searches for keywords
5. **Result Storage**: Results are stored in Redis with task ID
6. **Notification**: If matches found, email notification is sent
7. **Status Retrieval**: Client can check task status and results

### Keyword Matching

- **Case-insensitive** search
- **Exact word matching** (not partial)
- **Context extraction**: Returns sentences containing keywords
- **Snippet limiting**: Maximum 3 snippets per keyword

## 🐳 Docker Services

| Service       | Purpose         | Port        | Dependencies    |
| ------------- | --------------- | ----------- | --------------- |
| `web`         | Flask API       | 5000        | rabbitmq        |
| `worker`      | Celery Worker   | -           | rabbitmq, redis |
| `celery-beat` | Task Scheduler  | -           | rabbitmq, redis |
| `rabbitmq`    | Message Broker  | 5672, 15672 | -               |
| `redis`       | Results Backend | 6379        | -               |
| `flower`      | Monitoring      | 5555        | rabbitmq, redis |

## 🔒 Security Considerations

- **Input Validation**: All requests validated with Marshmallow schemas
- **URL Restrictions**: Consider implementing domain whitelist for production
- **Rate Limiting**: Add rate limiting for API endpoints
- **Email Security**: Use app passwords, never plain passwords
- **Network Security**: Run behind reverse proxy in production

## 🚢 Production Deployment

### Docker Compose Production

```yaml
# docker-compose.prod.yml
version: "3.8"
services:
  web:
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
    # Add nginx proxy, SSL certificates
```

### Scaling Workers

```bash
# Scale Celery workers
docker-compose up -d --scale worker=3
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Connection Refused Errors:**

```bash
# Check if services are running
docker-compose ps

# Restart services
docker-compose down && docker-compose up -d
```

**Task Not Processing:**

```bash
# Check worker logs
docker-compose logs worker

# Check RabbitMQ queues
docker-compose logs rabbitmq
```

**Email Not Sending:**

- Verify SMTP credentials
- Check firewall/antivirus blocking SMTP
- Ensure app passwords for Gmail

### Debug Mode

```bash
# Run with detailed logging
docker-compose logs -f worker
```

## 🎯 Roadmap

- [ ] Database persistence for task history
- [ ] Web dashboard for job management
- [ ] Webhook notifications
- [ ] Advanced keyword patterns (regex support)
- [ ] Multiple notification channels (Slack, Discord)
- [ ] API authentication and rate limiting
- [ ] Task result pagination
- [ ] Bulk URL submission

---

**Happy Scraping! 🕷️✨**
