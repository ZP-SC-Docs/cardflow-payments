import os

# Environment defaults for cardflow-prod. Override with env vars in staging.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://cardflow:Pa55w0rd-cardflow-prod@db.cardflow.internal:5432/cardflow",
)
SQLITE_PATH = os.environ.get("SQLITE_PATH", "/var/lib/cardflow/cardflow.db")

# Payment gateway (test mode until go-live)
STRIPE_SECRET_KEY = "sk_test_51Kx9ZmQ2cfDEMO0000000000000000000000000000000000000000000000000000000000000000000000000000000"
GATEWAY_WEBHOOK_SECRET = "whsec_cardflow_7f3c2a91e4b8d5c6a0f1e2d3c4b5a697"

# Internal service auth
JWT_SECRET = "cardflow-jwt-signing-key-2025"
ADMIN_API_KEY = "cf_admin_9d1c3b5a7e2f4061829ac5d7e1f3b2a4"

# Card vault encryption (AES-128, see payments.tokenise_card)
CARD_VAULT_KEY = b"k3ss1k-c4rdfl0w!"

# Finance exports
EXPORT_DIR = "/var/lib/cardflow/exports"
SETTLEMENT_BUCKET = "cardflow-settlements-prod"
