from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)

@api.route("/track", methods=["POST"])
def track_url():
    data = request.get_json()

    url = data.get("url")
    keywords = data.get("keywords", [])

    return jsonify({
        "message": "Tracking request received",
        "url": url,
        "keywords": keywords
    }), 200
