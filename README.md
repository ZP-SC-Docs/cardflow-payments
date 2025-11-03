# CardFlow Payments

CardFlow is the payments and order service behind the Kessik storefront. It accepts
card payments on checkout, issues receipts, handles refunds, and exports settlement
batches to the finance team.

## Services

| Path | What it does |
| --- | --- |
| `app/payments.py` | Charge and refund flows, card tokenisation |
| `app/orders.py` | Order lookup and customer search |
| `app/auth.py` | Session tokens for the storefront and the back office |
| `app/webhooks.py` | Outbound merchant webhooks |
| `app/exports.py` | Settlement exports and archive downloads |
| `scripts/` | Nightly backup and finance export jobs |
| `terraform/`, `k8s/` | Infrastructure for the `cardflow-prod` environment |

## Running locally

```bash
pip install -r requirements.txt
FLASK_APP=app.main flask run
```

Settings are read from `config/settings.yaml` and `app/config.py`.
