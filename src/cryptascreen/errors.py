# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Typed exceptions for the CryptaScreen SDK (same classes and codes as @cryptascreen/sdk)."""

from __future__ import annotations

from typing import Any

PLAN_LIMIT_CODES = (
    "SEAT_LIMIT_REACHED",
    "API_KEY_LIMIT_REACHED",
    "MONITORED_WALLET_LIMIT_REACHED",
    "BULK_LIMIT_REACHED",
    "feature_not_in_plan",
)


class CryptaScreenError(Exception):
    """Base exception for all CryptaScreen SDK errors.

    Attributes:
        message: Human-readable error message.
        status: HTTP status code (0 when no response was received).
        code: Machine code, e.g. ``AUTHENTICATION_ERROR``, ``VALIDATION_ERROR``, ``RATE_LIMIT_EXCEEDED``.
        request_id: ``X-Request-Id`` of the response, if any.
        details: Extra structured details.
    """

    def __init__(
        self,
        message: str,
        status: int = 0,
        code: str = "UNKNOWN_ERROR",
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id
        self.details = details

    @property
    def status_code(self) -> int:
        """Alias of :attr:`status`."""
        return self.status


class AuthenticationError(CryptaScreenError):
    """401 - invalid or missing API key."""

    def __init__(
        self, message: str = "Invalid or missing API key", request_id: str | None = None
    ) -> None:
        super().__init__(message, 401, "AUTHENTICATION_ERROR", request_id)


class RateLimitError(CryptaScreenError):
    """429 rate limit (retried automatically before it is raised).

    Attributes:
        reset_at: When the limit is expected to reset (now + Retry-After).
        retry_after_ms: Milliseconds to wait (Retry-After seconds, default 60000).
    """

    def __init__(self, reset_at: Any, retry_after_ms: int, request_id: str | None = None) -> None:
        super().__init__(
            f"Rate limit exceeded. Resets at {reset_at.isoformat()}",
            429,
            "RATE_LIMIT_EXCEEDED",
            request_id,
        )
        self.reset_at = reset_at
        self.retry_after_ms = retry_after_ms

    @property
    def retry_after(self) -> float:
        """Seconds to wait before retrying."""
        return self.retry_after_ms / 1000


class QuotaExceededError(CryptaScreenError):
    """429 ``quota_exceeded``: the plan's monthly screenings are used up. NOT a rate limit; never retried."""

    def __init__(
        self,
        message: str,
        request_id: str | None = None,
        resets_at: str | None = None,
        upgrade_url: str | None = None,
    ) -> None:
        super().__init__(
            message,
            429,
            "QUOTA_EXCEEDED",
            request_id,
            {"resetsAt": resets_at, "upgradeUrl": upgrade_url},
        )
        self.resets_at = resets_at
        self.upgrade_url = upgrade_url


class ServicePausedError(CryptaScreenError):
    """402 ``SERVICE_PAUSED``: a payment is overdue. Not retried."""

    def __init__(
        self,
        message: str,
        request_id: str | None = None,
        subscription_status: str | None = None,
        billing_url: str | None = None,
        reason: str | None = None,
    ) -> None:
        super().__init__(
            message,
            402,
            "SERVICE_PAUSED",
            request_id,
            {
                "subscriptionStatus": subscription_status,
                "billingUrl": billing_url,
                "reason": reason,
            },
        )
        self.subscription_status = subscription_status
        self.billing_url = billing_url
        self.reason = reason


class PlanLimitError(CryptaScreenError):
    """403 with a plan-limit code: an addition beyond the plan's entitlement was refused. Not retried."""

    def __init__(
        self,
        message: str,
        limit_code: str,
        request_id: str | None = None,
        used: int | None = None,
        limit: int | None = None,
        plan: str | None = None,
    ) -> None:
        super().__init__(
            message, 403, limit_code, request_id, {"used": used, "limit": limit, "plan": plan}
        )
        self.limit_code = limit_code
        self.used = used
        self.limit = limit
        self.plan = plan


class SeatLimitReachedError(PlanLimitError):
    """403 SEAT_LIMIT_REACHED."""

    def __init__(
        self,
        message: str,
        request_id: str | None = None,
        used: int | None = None,
        limit: int | None = None,
        plan: str | None = None,
    ) -> None:
        super().__init__(message, "SEAT_LIMIT_REACHED", request_id, used, limit, plan)


class ApiKeyLimitReachedError(PlanLimitError):
    """403 API_KEY_LIMIT_REACHED."""

    def __init__(
        self,
        message: str,
        request_id: str | None = None,
        used: int | None = None,
        limit: int | None = None,
        plan: str | None = None,
    ) -> None:
        super().__init__(message, "API_KEY_LIMIT_REACHED", request_id, used, limit, plan)


class NotFoundError(CryptaScreenError):
    """404 Not Found."""

    def __init__(
        self, resource: str = "Resource", id: str = "", request_id: str | None = None
    ) -> None:
        super().__init__(f"{resource} not found: {id}", 404, "NOT_FOUND", request_id)


class ValidationError(CryptaScreenError):
    """400 - request validation failed.

    Attributes:
        field_errors: ``{field: [messages]}``; bulk items appear as ``field[index]``.
        validation_code: e.g. UNKNOWN_CHAIN, INVALID_ADDRESS_FORMAT, INVALID_CHECKSUM, INVALID_BULK_ITEMS.
        items: Bulk: every invalid item (the whole request was rejected).
    """

    def __init__(
        self,
        message: str,
        field_errors: dict[str, list[str]] | None = None,
        request_id: str | None = None,
        validation_code: str | None = None,
        items: list[dict[str, Any]] | None = None,
    ) -> None:
        self.field_errors = field_errors or {}
        self.validation_code = validation_code
        self.items = items or []
        super().__init__(
            message,
            400,
            "VALIDATION_ERROR",
            request_id,
            {
                "fieldErrors": self.field_errors,
                "validationCode": validation_code,
                "items": self.items,
            },
        )
