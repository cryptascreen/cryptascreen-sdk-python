# Changelog

## 0.2.1

- Package metadata: author and maintainer are CryptaCount, Inc. (the copyright and licence holder, as in LICENSE). No code or API change.

## 0.2.0

- **BREAKING:** `chain` is now required on every screening call; the server returns 400 `CHAIN_REQUIRED` when it is missing. `screening.screen_address` needs `chain`, and `screen_bulk` / `screen_bulk_async` / `screen_bulk_and_wait` need `chains` (one per address); there is no default network. A missing or blank value raises `ValidationError` with `validation_code == "CHAIN_REQUIRED"` (checked before the request is sent, and mapped from the server's 400 as well). `ScreenAddressRequest.chain` and `BulkScreeningRequest.chains` have no default.
- New resources for the remaining customer API calls usable with an API key: `auth.me`, `capabilities.get`; `settings` (`get_score_thresholds`, `get_score_threshold_audit`, `get_name_matching`, `get_name_matching_audit`, `get_name_lists`, `get_name_list_audit`, `list_vendor_keys`); `monitoring` (`list_wallets`, `add_wallet`, `remove_wallet`, `list_names`, `add_name`, `remove_name`, `get_overview`, `list_breaches`, `get_breach_summary`, `acknowledge_breach`). Sync and async.
- Changing settings, the allow and block lists and vendor keys, and `auth/refresh`, need a signed-in user in the app and are not wrapped.
- Webhook models match the API (`WebhookConfig.is_active`, `WebhookDelivery.status`, ...); `webhooks.get_deliveries(webhook_id)` returns the last 50 deliveries as a list and takes no paging arguments. `CreateWebhookRequest` and `WebhookTestResult` are gone.
- The OpenAPI parity test now has no known gaps: every SDK method is an operation of the customer API contract.

## 0.1.0 — unreleased

First version of the CryptaScreen Python SDK. API surface = `@cryptascreen/sdk` 0.2.2 (every endpoint method usable with an API key 1:1, same
request/response fields, error classes and codes, retry policy), plus:

- requests go to `https://api.cryptascreen.com`, which routes them by the API key's data region (no region option),
- webhook signature verification (`verify_webhook_signature`, `construct_webhook_event`).

Naming: TS `screenAddress` -> `screen_address`, `CryptaScreenClient` -> `CryptaScreen` (alias `CryptaScreenClient` kept), options objects
-> keyword arguments, `retries` -> `max_retries`, `timeout` in seconds.

Notes found by the local contract run:

- `chains[i]` pairs with `addresses[i]`: the lists must have the same length (`400 addresses and chains lists must have the same length`).
- Webhooks: `webhooks.list` and `webhooks.get_deliveries` only. Registering, deleting and test-sending an endpoint require a signed-in user in the CryptaScreen app (an API key gets `403`), so this SDK does not offer them.
