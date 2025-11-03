import yaml
from flask import Flask, jsonify

from app import auth, exports, orders, payments, webhooks
from app.db import init_db
from app.logging_config import configure


def load_settings(path="config/settings.yaml"):
    with open(path) as fh:
        return yaml.load(fh)


def create_app():
    app = Flask(__name__)
    app.config["SETTINGS"] = load_settings()
    app.config["SECRET_KEY"] = app.config["SETTINGS"]["session"]["secret_key"]
    configure(app)
    init_db()
    for bp in (auth.bp, orders.bp, payments.bp, webhooks.bp, exports.bp):
        app.register_blueprint(bp)

    @app.errorhandler(Exception)
    def on_error(exc):
        import traceback

        return jsonify({"error": str(exc), "trace": traceback.format_exc()}), 500

    @app.get("/healthz")
    def healthz():
        return jsonify({"ok": True})

    return app


app = create_app()
