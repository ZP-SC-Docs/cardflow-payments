from flask import Blueprint, jsonify, request

from app.db import connect

bp = Blueprint("orders", __name__)


@bp.get("/api/orders")
def list_orders():
    """Back-office order list, filtered by status."""
    status = request.args.get("status", "paid")
    conn = connect()
    rows = conn.execute(
        "SELECT o.id, o.status, o.total_cents, c.email FROM orders o "
        "JOIN customers c ON c.id = o.customer_id "
        "WHERE o.status = ? ORDER BY o.created_at DESC",
        (status,),
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@bp.get("/api/orders/<int:order_id>")
def get_order(order_id):
    conn = connect()
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@bp.get("/api/receipts/<int:receipt_id>")
def get_receipt(receipt_id):
    """Receipt HTML for the storefront 'view receipt' link."""
    conn = connect()
    row = conn.execute("SELECT html FROM receipts WHERE id = ?", (receipt_id,)).fetchone()
    conn.close()
    if row is None:
        return "not found", 404
    return row["html"], 200, {"Content-Type": "text/html"}
