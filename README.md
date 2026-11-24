# CryptaScreen Python SDK

Official Python SDK for the [CryptaScreen API](https://github.com/cryptascreen/cryptascreen-sdk-python#readme) — address and name screening, sanctions, wallet exposure, investigations, webhooks.

[![Python 3.10-3.13](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Same API surface as the [TypeScript SDK](https://github.com/cryptascreen/cryptascreen-sdk-typescript) (`cryptascreen.operations.OPERATIONS` lists each one with its HTTP method and path).

## Installation

Supported Python versions: 3.10, 3.11, 3.12, 3.13.

```bash
pip install cryptascreen
```

With optional extras:

```bash
pip install cryptascreen[async]    # HTTP/2 support for the async client
pip install cryptascreen[dev]      # Development tools (pytest, mypy, ruff, respx)
```

## Quick Start

```python
from cryptascreen import CryptaScreen

client = CryptaScreen(api_key="csk_...")

result = client.screening.screen_address(
    {"address": "0x1111111111111111111111111111111111111111", "chain": "ethereum"}
)
print(result.risk_level, result.risk_score, result.sanctions_match)
# "no match" means no match in the layers listed in result.layers; check result.assessment_status before treating it as clear

client.close()
```

### Context Manager

```python
with CryptaScreen(api_key="csk_...") as client:
    status = client.sanctions.get_status()
```

### Async Client

```python
from cryptascreen import AsyncCryptaScreen

async with AsyncCryptaScreen(api_key="csk_...") as client:
    result = await client.screening.screen_address(
        {"address": "0x1111111111111111111111111111111111111111", "chain": "ethereum"}
    )
```

Requests may be plain dicts (camelCase wire names) or the typed models (`from cryptascreen.types import ScreenAddressRequest`).
Responses are pydantic models with snake_case attributes (`risk_level`, `evaluation_id`); unknown future fields are kept.

## Chain is required

`chain` is required on every screening call, single and bulk (`chains`, one per address). An address does not identify its
network, so there is no default. A missing or blank chain raises `ValidationError` with `validation_code == "CHAIN_REQUIRED"`.

## Data region

Every request goes to `https://api.cryptascreen.com`, which routes it to the data region of your API key
(`csk_us_...` keys to the US region, `csk_eu_...` keys to the EU region). There is no region option: use the key of the
region your account lives in.

```python
CryptaScreen(api_key="csk_eu_...")  # served by the EU region
CryptaScreen(
    api_key="csk_...", base_url="http://localhost:8081"
)  # optional: for example a proxy
```

## API Reference

### Screening

```python
r = client.screening.screen_address({"address": addr, "chain": "ethereum"})

# Bulk, synchronous (max 1000) - `async` is forced to False
results = client.screening.screen_bulk(
    {"addresses": [a1, a2], "chains": ["ethereum", "ethereum"]}
)  # chains[i] belongs to addresses[i]: equal lengths

# Bulk, asynchronous (max 10000): job + poll (an Idempotency-Key is always sent)
job = client.screening.screen_bulk_async({"addresses": addrs, "chains": ["ethereum"] * len(addrs)})
job = client.screening.poll_job(job.job_id)
job = client.screening.screen_bulk_and_wait(
    {"addresses": addrs, "chains": ["ethereum"] * len(addrs)}, poll_interval=2.0, timeout=300
)
page = client.screening.get_job_results(job.job_id, page=0, size=100)
client.screening.list_jobs()
client.screening.cancel_job(job.job_id)

# History and evaluations
client.screening.get_history("ethereum", addr)
client.screening.list_evaluations("ethereum", addr, page=0, size=20)
client.screening.get_evaluation(r.evaluation_id)

# Wallet sections and exposure (screened wallets only)
client.screening.get_counterparties("ethereum", addr, page=0, size=50, listed_only=True)
client.screening.get_transactions("ethereum", addr, direction="IN")
client.screening.get_exposure_paths("ethereum", addr, days=90)
```

### Sanctions

```python
client.sanctions.check("ethereum", addr)  # exact match against the self-hosted sanctions lists
client.sanctions.get_status()
```

### Name screening

```python
hit = client.names.screen(
    {"name": "Test Name", "type": "PERSON", "nationalities": ["LU"]}, idempotency_key="my-key"
)
from cryptascreen.helpers import is_name_clear

is_name_clear(hit)  # True only for outcome CLEAR; anything else needs a person to look
client.names.get(hit.screening_id)
client.names.history(limit=50)
client.names.decide({"hitId": "...", "value": "FALSE_POSITIVE", "reason": "different person"})
client.names.decision_audit(format="json")  # or "csv"
```

### Graph analysis

```python
g = client.graph.build_graph({"seedAddress": addr, "chain": "ethereum", "maxHops": 2})
client.graph.trace({"seedAddress": addr, "chain": "ethereum", "direction": "FORWARD"})
client.graph.export_graph({"seedAddress": addr, "chain": "ethereum"}, format="csv")  # bytes
```

### Investigation cases, alerts

```python
c = client.cases.create({"title": "Review", "addresses": []})
client.cases.list(status="OPEN", page=1)
client.cases.add_note(c.id, {"content": "looked at it"})
client.cases.set_assignee(c.id, 12)  # None = unassign
client.cases.link_evaluation(c.id, evaluation_id)
client.alerts.get(7)
client.alerts.acknowledge(7, "reviewed")
```

### Compliance and intelligence

```python
client.compliance.check_travel_rule({...})
client.compliance.identify_vasp("ethereum", addr)
client.intelligence.get_entity_labels("ethereum", addr)  # [] = no label known, NOT a clean verdict
```

### Account, capabilities, settings, monitoring

These calls accept an API key (plans without a feature get 403 `feature_not_in_plan`).

```python
client.auth.me()  # the calling identity (auth_method "API_KEY")
client.capabilities.get()  # chains the API accepts + live layer state

# Settings: read-only with an API key (changing them needs a signed-in tenant administrator, in the app)
client.settings.get_score_thresholds()  # review / block thresholds (defaults 40 / 70)
client.settings.get_score_threshold_audit(limit=20)
client.settings.get_name_matching()  # CONSERVATIVE | BALANCED | STRICT
client.settings.get_name_matching_audit()
client.settings.get_name_lists()  # allow / block entries
client.settings.get_name_list_audit()
client.settings.list_vendor_keys()  # configured state, last four characters, fingerprint; never a key

# Monitoring
client.monitoring.get_overview()
client.monitoring.add_wallet({"address": "0x...", "chain": "ethereum", "label": "treasury"})
client.monitoring.list_wallets()
client.monitoring.remove_wallet(1)
client.monitoring.add_name({"name": "Jane Doe"})
client.monitoring.list_names()
client.monitoring.remove_name(1)
client.monitoring.list_breaches()
client.monitoring.get_breach_summary()
client.monitoring.acknowledge_breach(1)
```

### Webhooks

```python
# registering, deleting and test-sending an endpoint is done by a signed-in user in the CryptaScreen app
hooks = client.webhooks.list()
client.webhooks.get_deliveries(hooks[0].id)  # the last 50 deliveries, newest first
```

Verify a delivery in your receiver (use the RAW body, not re-serialised JSON):

```python
from cryptascreen import WebhookSignatureError, construct_webhook_event

try:
    event = construct_webhook_event(
        secret, raw_body, request_headers
    )  # raises WebhookSignatureError
except WebhookSignatureError as e:
    ...  # e.code: WEBHOOK_SIGNATURE_MISSING | _MALFORMED | _MISMATCH | WEBHOOK_TIMESTAMP_OUT_OF_TOLERANCE
```

Scheme: header `X-CryptaScreen-Signature-V2: t=<unix>,v1=<hex(HMAC-SHA256(secret, "<unix>." + body))>`, timestamp
tolerance 300 s (configurable, `tolerance=`), constant-time comparison. The legacy `X-CryptaScreen-Signature: sha256=<hex>` header has no
timestamp and is accepted only with `allow_legacy=True`.

## Error Handling

```python
from cryptascreen import (
    AuthenticationError,
    CryptaScreenError,
    PlanLimitError,
    QuotaExceededError,
    RateLimitError,
    ServicePausedError,
    ValidationError,
)

try:
    client.screening.screen_address({"address": "0x123", "chain": "ethereum"})
except ValidationError as e:
    print(e.validation_code, e.field_errors, e.items)  # INVALID_ADDRESS_FORMAT ...
except QuotaExceededError as e:
    print(e.resets_at, e.upgrade_url)  # the monthly plan quota: not retried
except RateLimitError as e:
    print(e.retry_after_ms)
except CryptaScreenError as e:
    print(e.status, e.code, e.request_id)
```

| Status | Class | `code` |
|---|---|---|
| 400 | `ValidationError` | `VALIDATION_ERROR` |
| 401 | `AuthenticationError` | `AUTHENTICATION_ERROR` |
| 402 | `ServicePausedError` (`SERVICE_PAUSED`) / `CryptaScreenError` | `SERVICE_PAUSED` / `PAYMENT_REQUIRED` |
| 403 | `PlanLimitError` (`SeatLimitReachedError`, `ApiKeyLimitReachedError`) / `CryptaScreenError` | the limit code / `FORBIDDEN` |
| 404 | `NotFoundError` | `NOT_FOUND` |
| 429 | `RateLimitError` / `QuotaExceededError` | `RATE_LIMIT_EXCEEDED` / `QUOTA_EXCEEDED` |
| other | `CryptaScreenError` | the body's `code` or `UNKNOWN_ERROR` |

## Retry Logic

The SDK retries 429 (except `quota_exceeded`) and every 5xx up to `max_retries` (default 3). The delay is the `Retry-After`
header (integer seconds) when present, otherwise exponential backoff 1 s, 2 s, 4 s ... capped at 30 s. 400, 401, 402, 403, 404 and
the monthly quota are never retried; network errors are not retried (`CryptaScreenError`, status 0, `UNKNOWN_ERROR`).

## Development

```bash
pip install -e ".[dev]"
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/cryptascreen/ --ignore-missing-imports
pytest -v
python -m build                # sdist + wheel
```

## License

MIT - see [LICENSE](LICENSE).
