# Changelog

## 0.2.4 - 2026-11-24

First release on PyPI. Requires Python 3.10 to 3.13.

- Sync (`CryptaScreen`) and async clients for the CryptaScreen customer API: address and bulk screening, async jobs, evaluations and history, sanctions, name screening, wallet sections and exposure, graph, cases and alerts, compliance and intelligence.
- `chain` is required on every screening call; `screen_bulk`, `screen_bulk_async` and `screen_bulk_and_wait` take `chains`, one per address. A missing value raises `ValidationError` with `validation_code == "CHAIN_REQUIRED"`.
- `auth.me`, `capabilities.get`, `settings` (read-only with an API key) and `monitoring` (monitored wallets and names, overview, breaches).
- Webhooks: `webhooks.list` and `webhooks.get_deliveries` (last 50 deliveries), plus signature verification with `verify_webhook_signature` and `construct_webhook_event`. Registering, deleting and testing endpoints is done in the CryptaScreen app.
- Requests go to `https://api.cryptascreen.com`, which routes them by the API key's data region.
