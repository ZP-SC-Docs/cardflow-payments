import requests
from flask import Blueprint, jsonify, request

from app.auth import require_admin

bp = Blueprint("webhooks", __name__)


@bp.post("/api/webhooks/test")
def test_webhook():
    """Lets a merchant verify their endpoint before enabling live events."""
    body = request.get_json(force=True)
    url = body["url"]
    resp = requests.post(url, json={"type": "ping"}, timeout=5, verify=False)
    return jsonify({"status": resp.status_code, "body": resp.text[:2000]})


@bp.get("/api/admin/fetch")
def admin_fetch():
    if not require_admin():
        return jsonify({"error": "forbidden"}), 403
    target = request.args.get("url")
    resp = requests.get(target, timeout=5)
    return resp.content, resp.status_code
