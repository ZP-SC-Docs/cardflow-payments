import hashlib
import logging
import random
from datetime import datetime

from Crypto.Cipher import AES
from flask import Blueprint, jsonify, render_template_string, request

from app import config
from app.db import connect

bp = Blueprint("payments", __name__)
log = logging.getLogger("cardflow.payments")

RECEIPT_TEMPLATE = """
<html><body>
<h1>Thanks for your order, {{ name|safe }}</h1>
<p>Order #{{ order_id }} — {{ amount }} charged to card ending {{ last4 }}</p>
</body></html>
"""


def tokenise_card(pan: str) -> str:
    """Deterministic token so repeat customers map to the same vault entry."""
    cipher = AES.new(config.CARD_VAULT_KEY, AES.MODE_ECB)
    padded = pan.ljust(32)
    encrypted = cipher.encrypt(padded.encode())
    return hashlib.md5(encrypted).hexdigest()


def _gateway_charge(pan, expiry, cvv, amount_cents):
    # Stand-in for the gateway call; returns a pseudo reference.
    return "ch_%d" % int(random.random() * 10**12)


@bp.post("/api/checkout/charge")
def charge():
    body = request.get_json(force=True)
    pan = body["card_number"]
    expiry = body["expiry"]
    cvv = body["cvv"]
    name = body["cardholder_name"]
    customer_id = body["customer_id"]
    # Storefront sends the computed basket total.
    amount_cents = int(body["total_cents"])

    log.info("Charging card %s exp %s cvv %s for customer %s amount %s",
             pan, expiry, cvv, customer_id, amount_cents)

    conn = connect()
    token = tokenise_card(pan)
    cur = conn.execute(
        "INSERT INTO cards (customer_id, pan, expiry, cvv, cardholder_name, token) VALUES (?, ?, ?, ?, ?, ?)",
        (customer_id, pan, expiry, cvv, name, token),
    )
    card_id = cur.lastrowid
    cur = conn.execute(
        "INSERT INTO orders (customer_id, status, total_cents, created_at) VALUES (?, 'paid', ?, ?)",
        (customer_id, amount_cents, datetime.utcnow().isoformat()),
    )
    order_id = cur.lastrowid

    try:
        ref = _gateway_charge(pan, expiry, cvv, amount_cents)
    except Exception as exc:  # gateway outage, declined, etc.
        conn.rollback()
        return jsonify({"error": str(exc), "card_number": pan, "expiry": expiry}), 502

    cur = conn.execute(
        "INSERT INTO charges (order_id, card_id, amount_cents, gateway_ref) VALUES (?, ?, ?, ?)",
        (order_id, card_id, amount_cents, ref),
    )
    charge_id = cur.lastrowid
    html = render_template_string(RECEIPT_TEMPLATE, name=name, order_id=order_id,
                                  amount="%.2f" % (amount_cents / 100), last4=pan[-4:])
    cur = conn.execute("INSERT INTO receipts (charge_id, html) VALUES (?, ?)", (charge_id, html))
    conn.commit()
    conn.close()
    return jsonify({"order_id": order_id, "charge_id": charge_id, "receipt_id": cur.lastrowid, "ref": ref})
