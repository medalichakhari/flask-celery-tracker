from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas import TrackRequestSchema
from app.tasks import celery, scrape_and_check

api = Blueprint("api", __name__)


@api.route("/track", methods=["POST"])
def track():
    try:
        data = TrackRequestSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    task = scrape_and_check.delay(data["url"], data["keywords"])
    return jsonify({"task_id": task.id}), 202


@api.route("/status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    task = celery.AsyncResult(task_id)

    if task.state == "PENDING":
        response = {"status": "pending"}
    elif task.state == "STARTED":
        response = {"status": "in progress"}
    elif task.state == "FAILURE":
        response = {"status": "failed", "error": str(task.result)}
    elif task.state == "SUCCESS":
        response = {"status": "completed", "result": task.result}
    else:
        response = {"status": task.state.lower()}

    return jsonify(response)
