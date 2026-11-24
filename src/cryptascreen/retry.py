"""Retry policy and error mapping (same as @cryptascreen/sdk client.ts).

Retry on 429 (except ``quota_exceeded``) and on any 5xx, up to ``max_retries``. Delay: the ``Retry-After`` header
(integer seconds) when present, otherwise exponential 1s, 2s, 4s ... capped at 30s. Never retried: 400, 401, 402, 403, 404,
429 ``quota_exceeded``. Network errors are not retried.
"""

from __future__ import annotations

import asyncio
import re
import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from cryptascreen.config import Config
from cryptascreen.errors import (
    PLAN_LIMIT_CODES,
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


def _body(response: httpx.Response) -> dict[str, Any]:
    try:
        data = response.json()
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def is_quota_exceeded(response: httpx.Response) -> bool:
    """429 ``quota_exceeded`` is the plan's monthly cap, not a rate limit."""
    if response.status_code != 429:
        return False
    body = _body(response)
    return body.get("error") == "quota_exceeded" or body.get("code") == "QUOTA_EXCEEDED"


def is_retryable(response: httpx.Response) -> bool:
    status = response.status_code
    return (status == 429 and not is_quota_exceeded(response)) or status >= 500


def _parse_int(value: str | None) -> int | None:
    """JavaScript ``parseInt(value, 10)``: leading integer, otherwise None."""
    if value is None:
        return None
    m = re.match(r"\s*([+-]?\d+)", value)
    return int(m.group(1)) if m else None


def retry_delay(response: httpx.Response, attempt: int, config: Config) -> float:
    """Seconds to wait before retry number ``attempt + 1``."""
    seconds = _parse_int(response.headers.get("retry-after"))
    if seconds is not None:
        return max(0.0, float(seconds))
    return float(min(config.retry_base_delay * (2**attempt), config.retry_max_delay))


def to_sdk_error(response: httpx.Response) -> CryptaScreenError:
    """Map an error response to a typed exception (client.ts ``toSdkError``)."""
    status = response.status_code
    body = _body(response)
    request_id = response.headers.get("x-request-id")
    raw_message = body.get("message")
    message: str = (
        raw_message if isinstance(raw_message, str) else f"Request failed with status code {status}"
    )

    if status == 401:
        return AuthenticationError(message, request_id)
    if status == 404:
        return NotFoundError(
            str(body.get("resource") or "Resource"), str(body.get("id") or ""), request_id
        )
    if status == 400:
        field_errors: dict[str, list[str]] = {
            k: list(v) for k, v in (body.get("fieldErrors") or {}).items()
        }
        field = body.get("field")
        if field:
            field_errors[field] = [*field_errors.get(field, []), message]
        items = body.get("items") or []
        for it in items:
            key = f"{it.get('field')}[{it.get('index')}]"
            field_errors[key] = [*field_errors.get(key, []), it.get("message")]
        return ValidationError(message, field_errors, request_id, body.get("code"), items)
    if status == 403:
        code = body.get("error") or body.get("code")
        if code and code in PLAN_LIMIT_CODES:
            used, limit, plan = body.get("used"), body.get("limit"), body.get("plan")
            if code == "SEAT_LIMIT_REACHED":
                return SeatLimitReachedError(message, request_id, used, limit, plan)
            if code == "API_KEY_LIMIT_REACHED":
                return ApiKeyLimitReachedError(message, request_id, used, limit, plan)
            return PlanLimitError(message, code, request_id, used, limit, plan)
        return CryptaScreenError(
            message, 403, body.get("code") or body.get("error") or "FORBIDDEN", request_id, body
        )
    if status == 402:
        if body.get("code") == "SERVICE_PAUSED" or body.get("error") == "service_paused":
            return ServicePausedError(
                message,
                request_id,
                body.get("subscriptionStatus"),
                body.get("billing_url"),
                body.get("reason"),
            )
        return CryptaScreenError(
            message, 402, body.get("code") or "PAYMENT_REQUIRED", request_id, body
        )
    if status == 429:
        if is_quota_exceeded(response):
            return QuotaExceededError(
                message, request_id, body.get("resets_at"), body.get("upgrade_url")
            )
        parsed = _parse_int(response.headers.get("retry-after"))
        retry_after_ms = parsed * 1000 if parsed is not None else 60_000
        reset_at = datetime.now(timezone.utc) + timedelta(milliseconds=retry_after_ms)
        return RateLimitError(reset_at, retry_after_ms, request_id)
    return CryptaScreenError(
        message, status, body.get("code") or "UNKNOWN_ERROR", request_id, body or None
    )


def transport_error(exc: Exception) -> CryptaScreenError:
    """No response (timeout, connection error): TS maps this to UNKNOWN_ERROR / status 0, never retried."""
    return CryptaScreenError(str(exc) or exc.__class__.__name__, 0, "UNKNOWN_ERROR")


def execute_with_retry(config: Config, request: Callable[[], httpx.Response]) -> httpx.Response:
    """Run ``request`` with the SDK retry policy; raise a typed error on failure."""
    attempt = 0
    while True:
        try:
            response = request()
        except httpx.HTTPError as exc:
            raise transport_error(exc) from exc
        if response.is_success:
            return response
        if is_retryable(response) and attempt < config.max_retries:
            time.sleep(retry_delay(response, attempt, config))
            attempt += 1
            continue
        raise to_sdk_error(response)


async def async_execute_with_retry(
    config: Config, request: Callable[[], Awaitable[httpx.Response]]
) -> httpx.Response:
    """Async variant of :func:`execute_with_retry`."""
    attempt = 0
    while True:
        try:
            response = await request()
        except httpx.HTTPError as exc:
            raise transport_error(exc) from exc
        if response.is_success:
            return response
        if is_retryable(response) and attempt < config.max_retries:
            await asyncio.sleep(retry_delay(response, attempt, config))
            attempt += 1
            continue
        raise to_sdk_error(response)
