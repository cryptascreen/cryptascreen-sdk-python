"""Webhook signature verification.

CryptaScreen signs every webhook delivery twice:

* ``X-CryptaScreen-Signature-V2: t=<unix>,v1=<hex(HMAC_SHA256(secret, "<unix>." + body))>`` (replay-resistant)
* ``X-CryptaScreen-Signature: sha256=<hex(HMAC_SHA256(secret, body))>`` (legacy, no timestamp)

``verify_webhook_signature`` checks V2 (constant-time compare, timestamp within ``tolerance`` seconds, default 300).
The legacy header is accepted only with ``allow_legacy=True`` (it cannot detect a replay). The same algorithm and test
vectors (``tests/fixtures/webhook_vectors.json``) are used by the other CryptaScreen SDKs.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import time
from typing import Any

from cryptascreen.errors import CryptaScreenError

SIGNATURE_HEADER = "X-CryptaScreen-Signature"
SIGNATURE_V2_HEADER = "X-CryptaScreen-Signature-V2"
TIMESTAMP_HEADER = "X-CryptaScreen-Timestamp"
EVENT_HEADER = "X-CryptaScreen-Event"
EVENT_ID_HEADER = "X-CryptaScreen-Event-Id"
DEFAULT_TOLERANCE_SECONDS = 300


class WebhookSignatureError(CryptaScreenError):
    """The webhook payload could not be authenticated (``code`` says why)."""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message, 0, code)


def compute_webhook_signature(secret: str, body: str | bytes, timestamp: int | None = None) -> str:
    """Hex HMAC-SHA256: of ``body`` (legacy) or of ``"<timestamp>." + body`` when a timestamp is given."""
    raw = body.encode("utf-8") if isinstance(body, str) else body
    msg = raw if timestamp is None else f"{timestamp}.".encode() + raw
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


def _header(headers: Any, name: str) -> str | None:
    lname = name.lower()
    for k in headers:
        if str(k).lower() == lname:
            v = headers[k]
            return v if isinstance(v, str) else (v[0] if v else None)
    return None


def verify_webhook_signature(
    secret: str,
    body: str | bytes,
    headers: Any,
    *,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
    allow_legacy: bool = False,
    now: float | None = None,
) -> bool:
    """Return True when the delivery is authentic; raise :class:`WebhookSignatureError` otherwise.

    Args:
        secret: The webhook secret (``WebhookConfig.secret``).
        body: The RAW request body exactly as received (not re-serialised JSON).
        headers: Mapping of request headers (case-insensitive lookup).
        tolerance: Maximum clock difference in seconds between ``t`` and ``now`` (both directions).
        allow_legacy: Accept the legacy ``X-CryptaScreen-Signature`` header when no V2 header is present.
        now: Unix time override (tests).
    """
    v2 = _header(headers, SIGNATURE_V2_HEADER)
    current = time.time() if now is None else now
    if v2:
        parts = [p.strip() for p in v2.split(",")]
        t_raw = next((p[2:] for p in parts if p.startswith("t=")), None)
        sigs = [p[3:] for p in parts if p.startswith("v1=")]
        if t_raw is None or not re.fullmatch(r"[0-9]{1,15}", t_raw) or not sigs:
            raise WebhookSignatureError(
                "Malformed X-CryptaScreen-Signature-V2 header", "WEBHOOK_SIGNATURE_MALFORMED"
            )
        t = int(t_raw)
        expected = compute_webhook_signature(secret, body, t)
        if not any(hmac.compare_digest(expected.encode(), s.lower().encode()) for s in sigs):
            raise WebhookSignatureError(
                "Webhook signature does not match", "WEBHOOK_SIGNATURE_MISMATCH"
            )
        if abs(current - t) > tolerance:
            raise WebhookSignatureError(
                f"Webhook timestamp outside the tolerance of {tolerance}s",
                "WEBHOOK_TIMESTAMP_OUT_OF_TOLERANCE",
            )
        return True
    legacy = _header(headers, SIGNATURE_HEADER)
    if legacy and allow_legacy:
        if not legacy.startswith("sha256="):
            raise WebhookSignatureError(
                "Malformed X-CryptaScreen-Signature header", "WEBHOOK_SIGNATURE_MALFORMED"
            )
        expected = compute_webhook_signature(secret, body)
        if not hmac.compare_digest(expected.encode(), legacy[7:].lower().encode()):
            raise WebhookSignatureError(
                "Webhook signature does not match", "WEBHOOK_SIGNATURE_MISMATCH"
            )
        return True
    raise WebhookSignatureError(
        "No usable signature header (X-CryptaScreen-Signature-V2)", "WEBHOOK_SIGNATURE_MISSING"
    )


def construct_webhook_event(
    secret: str, body: str | bytes, headers: Any, **kwargs: Any
) -> dict[str, Any]:
    """Verify (see :func:`verify_webhook_signature`) and return the parsed event ``{id, type, createdAt, source, data}``."""
    verify_webhook_signature(secret, body, headers, **kwargs)
    return json.loads(body)  # type: ignore[no-any-return]
