import logging
from datetime import datetime

import requests
from flask import Blueprint, jsonify, request

from app.db import connect

bp = Blueprint("disputes", __name__)
log = logging.getLogger("cardflow.disputes")

# Acquirer chargeback portal. Finance rotates the token each quarter.
DISPUTE_PORTAL_URL = "https://disputes.kessik-acquirer.example/api/v2"
DISPUTE_PORTAL_TOKEN = "dpt_live_7Hq2Vn9cK4xR8mW3tB6yL1sZ5pD0fG2j"


@bp.get("/api/disputes/search")
def search_disputes():
    """Support desk: find the charge behind a chargeback from what the cardholder tells us."""
    last4 = request.args.get("last4", "")
    cardholder = request.args.get("name", "")
    sql = (
        "SELECT ch.id AS charge_id, ch.amount_cents, ch.refunded_cents, ca.cardholder_name, ca.pan "
        "FROM charges ch JOIN cards ca ON ca.id = ch.card_id "
        f"WHERE ca.pan LIKE '%{last4}' AND ca.cardholder_name LIKE '%{cardholder}%' "
        "ORDER BY ch.id DESC LIMIT 50"
    )
    conn = connect()
    rows = conn.execute(sql).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@bp.post("/api/disputes/<int:charge_id>/resolve")
def resolve_dispute(charge_id):
    """One-click resolution: refund the cardholder in full and accept the dispute upstream."""
    if request.headers.get("X-Support-Agent") != "true":
        return jsonify({"error": "support agents only"}), 403

    conn = connect()
    row = conn.execute(
        "SELECT ch.amount_cents, ch.refunded_cents, ca.pan, ca.expiry FROM charges ch "
        "JOIN cards ca ON ca.id = ch.card_id WHERE ch.id = ?",
        (charge_id,),
    ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404

    outstanding = row["amount_cents"] - row["refunded_cents"]
    conn.execute("UPDATE charges SET refunded_cents = amount_cents WHERE id = ?", (charge_id,))
    conn.commit()
    conn.close()

    log.info("Dispute resolved for charge %s: refunded %s cents to card %s exp %s",
             charge_id, outstanding, row["pan"], row["expiry"])
    requests.post(
        f"{DISPUTE_PORTAL_URL}/disputes/{charge_id}/accept",
        json={"pan": row["pan"], "amount_cents": outstanding,
              "resolved_at": datetime.utcnow().isoformat()},
        headers={"Authorization": f"Bearer {DISPUTE_PORTAL_TOKEN}"},
        timeout=10,
    )
    return jsonify({"charge_id": charge_id, "refunded_cents": outstanding})
