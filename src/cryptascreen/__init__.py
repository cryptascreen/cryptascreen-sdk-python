# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""CryptaScreen Python SDK - official client for the CryptaScreen API.

Usage::

    from cryptascreen import CryptaScreen

    client = CryptaScreen(api_key="csk_...")
    result = client.screening.screen_address({"address": "0x...", "chain": "ethereum"})

For async usage::

    from cryptascreen import AsyncCryptaScreen

    async with AsyncCryptaScreen(api_key="csk_...") as client:
        result = await client.screening.screen_address({"address": "0x...", "chain": "ethereum"})
"""

from cryptascreen._util import generate_idempotency_key, is_terminal_job_status
from cryptascreen._version import __version__
from cryptascreen.client import AsyncCryptaScreen, CryptaScreen, CryptaScreenClient
from cryptascreen.errors import (
    ApiKeyLimitReachedError,
    AuthenticationError,
    CryptaScreenError,
    NotFoundError,
    PlanLimitError,
    QuotaExceededError,
    RateLimitError,
    SeatLimitReachedError,
    ServicePausedError,
    ValidationError,
)
from cryptascreen.signature import (
    WebhookSignatureError,
    compute_webhook_signature,
    construct_webhook_event,
    verify_webhook_signature,
)

__all__ = [
    "ApiKeyLimitReachedError",
    "AsyncCryptaScreen",
    "AuthenticationError",
    "CryptaScreen",
    "CryptaScreenClient",
    "CryptaScreenError",
    "NotFoundError",
    "PlanLimitError",
    "QuotaExceededError",
    "RateLimitError",
    "SeatLimitReachedError",
    "ServicePausedError",
    "ValidationError",
    "WebhookSignatureError",
    "__version__",
    "compute_webhook_signature",
    "construct_webhook_event",
    "generate_idempotency_key",
    "is_terminal_job_status",
    "verify_webhook_signature",
]
