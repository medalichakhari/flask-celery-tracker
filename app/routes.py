from flask import Blueprint, request, jsonify
from app.tasks import scrape_and_check

api = Blueprint("api", __name__)

@api.route("/track", methods=["POST"])
def track_url():
    data = request.get_json() or {}

    url = data.get("url")
    keywords = data.get("keywords")

    if not url or not keywords or not isinstance(keywords, list):
        return jsonify({"error": "Please provide 'url' and list of 'keywords'"}), 400

    task = scrape_and_check.delay(url, keywords)

    return jsonify({
        "message": "Tracking task created",
        "task_id": task.id
    }), 202
