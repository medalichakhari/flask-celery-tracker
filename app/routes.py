from flask import Blueprint, jsonify, request

from app.tasks import celery, scrape_and_check

api = Blueprint("api", __name__)


@api.route("/track", methods=["POST"])
def track_url():
    data = request.get_json() or {}

    url = data.get("url")
    keywords = data.get("keywords")

    if not url or not keywords or not isinstance(keywords, list):
        return jsonify({"error": "Please provide 'url' and list of 'keywords'"}), 400

    task = scrape_and_check.delay(url, keywords)

    return jsonify({"message": "Tracking task created", "task_id": task.id}), 202


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
