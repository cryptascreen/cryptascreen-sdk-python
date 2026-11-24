"""Client construction, headers, errors and the retry policy (same as @cryptascreen/sdk)."""

from __future__ import annotations

import httpx
import pytest

import cryptascreen
from cryptascreen import (
    ApiKeyLimitReachedError,
    AuthenticationError,
    CryptaScreen,
    CryptaScreenError,
    NotFoundError,
    PlanLimitError,
    QuotaExceededError,
    RateLimitError,
    SeatLimitReachedError,
    ServicePausedError,
    ValidationError,
)
from cryptascreen.config import DEFAULT_BASE_URL

from .conftest import TEST_ADDRESS, Recorder, make_client


def err(status: int, body: dict | None = None, headers: dict | None = None) -> httpx.Response:
    return httpx.Response(status, json=body if body is not None else {}, headers=headers or {})


def test_api_key_required() -> None:
    with pytest.raises(ValueError):
        CryptaScreen(api_key="")


def test_default_base_url_is_the_ts_default() -> None:
    assert DEFAULT_BASE_URL == "https://api.cryptascreen.com"
    assert CryptaScreen(api_key="k")._config.base_url == "https://api.cryptascreen.com"


def test_one_host_routes_by_the_key_and_there_is_no_region_option() -> None:
    assert (
        CryptaScreen(api_key="csk_eu_" + "0" * 32)._config.base_url
        == "https://api.cryptascreen.com"
    )
    assert (
        CryptaScreen(api_key="k", base_url="http://localhost:1")._config.base_url
        == "http://localhost:1"
    )
    with pytest.raises(TypeError):
        CryptaScreen(api_key="k", region="us")  # type: ignore[call-arg]


def test_headers_and_version() -> None:
    r = Recorder([httpx.Response(200, json=[])])
    make_client(r).screening.list_jobs()
    h = r.last.headers
    assert h["x-api-key"] == "csk_test"
    assert h["accept"] == "application/json"
    assert h["user-agent"] == f"cryptascreen-python/{cryptascreen.__version__}"


def test_alias_matches_ts_class_name() -> None:
    assert cryptascreen.CryptaScreenClient is CryptaScreen


@pytest.mark.parametrize(
    "status,body,cls,code",
    [
        (401, {"message": "bad key"}, AuthenticationError, "AUTHENTICATION_ERROR"),
        (404, {"resource": "Case", "id": "c1"}, NotFoundError, "NOT_FOUND"),
        (
            400,
            {"message": "bad", "code": "UNKNOWN_CHAIN", "field": "chain"},
            ValidationError,
            "VALIDATION_ERROR",
        ),
        (
            403,
            {
                "error": "BULK_LIMIT_REACHED",
                "message": "m",
                "used": 1,
                "limit": 1,
                "plan": "STARTER",
            },
            PlanLimitError,
            "BULK_LIMIT_REACHED",
        ),
        (
            403,
            {"error": "SEAT_LIMIT_REACHED", "message": "m"},
            SeatLimitReachedError,
            "SEAT_LIMIT_REACHED",
        ),
        (
            403,
            {"error": "API_KEY_LIMIT_REACHED", "message": "m"},
            ApiKeyLimitReachedError,
            "API_KEY_LIMIT_REACHED",
        ),
        (
            403,
            {"error": "CSRF_TOKEN_INVALID", "message": "m"},
            CryptaScreenError,
            "CSRF_TOKEN_INVALID",
        ),
        (
            402,
            {
                "code": "SERVICE_PAUSED",
                "message": "pay",
                "subscriptionStatus": "past_due",
                "billing_url": "u",
                "reason": "PAST_DUE",
            },
            ServicePausedError,
            "SERVICE_PAUSED",
        ),
        (402, {"message": "x"}, CryptaScreenError, "PAYMENT_REQUIRED"),
        (
            429,
            {
                "error": "quota_exceeded",
                "message": "cap",
                "resets_at": "2026-12-01T00:00:00Z",
                "upgrade_url": "u",
            },
            QuotaExceededError,
            "QUOTA_EXCEEDED",
        ),
        (
            409,
            {"code": "JOB_ALREADY_TERMINAL", "message": "done"},
            CryptaScreenError,
            "JOB_ALREADY_TERMINAL",
        ),
        (418, {}, CryptaScreenError, "UNKNOWN_ERROR"),
    ],
)
def test_error_mapping(status: int, body: dict, cls: type, code: str) -> None:
    r = Recorder([err(status, body, {"x-request-id": "rid-1"})])
    with pytest.raises(cls) as ei:
        make_client(r).sanctions.get_status()
    e = ei.value
    assert type(e) is cls
    assert e.status == status and e.code == code and e.request_id == "rid-1"
    assert len(r.requests) == 1, "non-retryable status must not be retried"


def test_validation_error_field_errors_and_bulk_items() -> None:
    body = {
        "message": "bad item",
        "code": "INVALID_BULK_ITEMS",
        "field": "addresses",
        "items": [
            {"index": 2, "field": "addresses", "code": "INVALID_CHECKSUM", "message": "checksum"}
        ],
    }
    with pytest.raises(ValidationError) as ei:
        make_client(Recorder([err(400, body)])).screening.screen_bulk(
            {"addresses": ["0x1"], "chains": ["ethereum"]}
        )
    e = ei.value
    assert e.validation_code == "INVALID_BULK_ITEMS"
    assert e.field_errors == {"addresses": ["bad item"], "addresses[2]": ["checksum"]}
    assert e.items[0]["code"] == "INVALID_CHECKSUM"


def test_quota_and_service_paused_fields() -> None:
    with pytest.raises(QuotaExceededError) as q:
        make_client(
            Recorder(
                [
                    err(
                        429,
                        {
                            "error": "quota_exceeded",
                            "message": "m",
                            "resets_at": "R",
                            "upgrade_url": "U",
                        },
                    )
                ]
            )
        ).sanctions.get_status()
    assert (q.value.resets_at, q.value.upgrade_url) == ("R", "U")
    with pytest.raises(ServicePausedError) as s:
        make_client(
            Recorder(
                [
                    err(
                        402,
                        {
                            "code": "SERVICE_PAUSED",
                            "message": "m",
                            "subscriptionStatus": "unpaid",
                            "billing_url": "B",
                            "reason": "PERIOD_NOT_PAID",
                        },
                    )
                ]
            )
        ).sanctions.get_status()
    assert (s.value.subscription_status, s.value.billing_url, s.value.reason) == (
        "unpaid",
        "B",
        "PERIOD_NOT_PAID",
    )


# ---- retry policy ---------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("status", [429, 500, 501, 502, 503, 504])
def test_retries_429_and_5xx_then_succeeds(status: int) -> None:
    r = Recorder(
        [
            err(status),
            err(status),
            httpx.Response(200, json={"total_active": 1, "by_source": {}, "last_checked": "t"}),
        ]
    )
    out = make_client(r).sanctions.get_status()
    assert out.total_active == 1
    assert len(r.requests) == 3


def test_gives_up_after_max_retries_429_rate_limit() -> None:
    r = Recorder([err(429, {}, {"retry-after": "0"})])
    with pytest.raises(RateLimitError) as ei:
        make_client(r, max_retries=3).sanctions.get_status()
    assert len(r.requests) == 4  # 1 + 3 retries
    assert ei.value.retry_after_ms == 0 and ei.value.code == "RATE_LIMIT_EXCEEDED"


def test_5xx_after_max_retries_is_cryptascreen_error() -> None:
    r = Recorder([err(503, {"message": "down"})])
    with pytest.raises(CryptaScreenError) as ei:
        make_client(r, max_retries=2).sanctions.get_status()
    assert len(r.requests) == 3 and ei.value.status == 503


@pytest.mark.parametrize(
    "status,body",
    [
        (401, {}),
        (402, {"code": "SERVICE_PAUSED"}),
        (403, {"error": "BULK_LIMIT_REACHED"}),
        (404, {}),
        (400, {}),
        (429, {"error": "quota_exceeded"}),
        (429, {"code": "QUOTA_EXCEEDED"}),
    ],
)
def test_never_retried(status: int, body: dict) -> None:
    r = Recorder([err(status, body)])
    with pytest.raises(CryptaScreenError):
        make_client(r).sanctions.get_status()
    assert len(r.requests) == 1


def test_retry_after_header_drives_the_delay_and_backoff_is_1_2_4(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("cryptascreen.retry.time.sleep", sleeps.append)
    r = Recorder([err(429, {}, {"retry-after": "7"}), err(503), err(503), err(503)])
    with pytest.raises(CryptaScreenError):
        make_client(r, max_retries=3, retry_base_delay=1.0).sanctions.get_status()
    assert sleeps == [7.0, 2.0, 4.0]  # attempt 0 uses Retry-After; attempts 1,2 use 1s*2^attempt


def test_backoff_is_capped_at_30s(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("cryptascreen.retry.time.sleep", sleeps.append)
    r = Recorder([err(500)])
    with pytest.raises(CryptaScreenError):
        make_client(r, max_retries=7, retry_base_delay=1.0).sanctions.get_status()
    assert sleeps == [1.0, 2.0, 4.0, 8.0, 16.0, 30.0, 30.0]


def test_non_numeric_retry_after_falls_back_to_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("cryptascreen.retry.time.sleep", sleeps.append)
    r = Recorder(
        [
            err(429, {}, {"retry-after": "Wed, 21 Oct 2026 07:28:00 GMT"}),
            httpx.Response(200, json={"total_active": 0, "by_source": {}, "last_checked": "t"}),
        ]
    )
    make_client(r, retry_base_delay=1.0).sanctions.get_status()
    assert sleeps == [1.0]


def test_rate_limit_error_defaults_to_60s_without_header() -> None:
    r = Recorder([err(429)])
    with pytest.raises(RateLimitError) as ei:
        make_client(r, max_retries=0).sanctions.get_status()
    assert ei.value.retry_after_ms == 60_000


def test_transport_error_is_unknown_error_and_not_retried() -> None:
    def boom(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused")

    r = Recorder(boom)
    with pytest.raises(CryptaScreenError) as ei:
        make_client(r).sanctions.get_status()
    assert ei.value.status == 0 and ei.value.code == "UNKNOWN_ERROR" and len(r.requests) == 1


async def test_async_client_same_policy() -> None:
    from cryptascreen.client import AsyncCryptaScreen, AsyncHttpClient
    from cryptascreen.config import Config
    from cryptascreen.resources.sanctions import AsyncSanctionsResource

    r = Recorder(
        [
            err(500),
            httpx.Response(200, json={"total_active": 2, "by_source": {}, "last_checked": "t"}),
        ]
    )
    http = AsyncHttpClient(
        Config(api_key="k", base_url="https://x.test", retry_base_delay=0.0),
        transport=httpx.MockTransport(r),
    )
    out = await AsyncSanctionsResource(http).get_status()
    assert out.total_active == 2 and len(r.requests) == 2
    c = AsyncCryptaScreen(api_key="k")
    assert c._config.base_url == "https://api.cryptascreen.com"
    await c.close()
    assert TEST_ADDRESS
