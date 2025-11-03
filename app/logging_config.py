import logging
import logging.handlers

LOG_PATH = "/var/log/cardflow/app.log"


def configure(app):
    handler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=50_000_000, backupCount=30)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    @app.before_request
    def log_request():
        from flask import request

        # Full request capture for support investigations.
        app.logger.debug("REQ %s %s headers=%s body=%s", request.method, request.path,
                         dict(request.headers), request.get_data(as_text=True))
