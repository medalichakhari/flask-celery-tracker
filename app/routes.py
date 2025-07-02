from datetime import timedelta
from typing import Any, Dict
from uuid import uuid4

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas import ScheduleRequestSchema, TrackRequestSchema
from app.tasks import celery, scrape_and_check

api = Blueprint("api", __name__)

track_schema = TrackRequestSchema()
schedule_schema = ScheduleRequestSchema()


def task_status_response(task: Any) -> Dict[str, Any]:
    state_map = {
        "PENDING": "pending",
        "STARTED": "in progress",
        "FAILURE": "failed",
        "SUCCESS": "completed",
    }
    status = state_map.get(task.state, task.state.lower())
    response = {"status": status}

    if status == "failed":
        response["error"] = str(task.result)
    elif status == "completed":
        response["result"] = task.result

    return response


@api.route("/track", methods=["POST"])
def track():
    try:
        data = track_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    task = scrape_and_check.delay(data["url"], data["keywords"])
    return jsonify({"task_id": task.id}), 202


@api.route("/status/<task_id>", methods=["GET"])
def get_task_status(task_id: str):
    task = celery.AsyncResult(task_id)
    response = task_status_response(task)
    return jsonify(response)


@api.route("/track/schedule", methods=["POST"])
def schedule_scrape():
    try:
        data = schedule_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    job_name = f"scrape-{uuid4().hex}"

    celery.conf.beat_schedule[job_name] = {
        "task": "app.tasks.scrape_and_check",
        "schedule": timedelta(minutes=data["interval_minutes"]),
        "args": (data["url"], data["keywords"]),
    }

    return jsonify(
        {
            "message": f"Scheduled scraping every {data['interval_minutes']} minutes.",
            "job_name": job_name,
        }
    )
