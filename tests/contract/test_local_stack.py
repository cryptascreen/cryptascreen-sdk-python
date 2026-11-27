# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Contract tests against a LOCAL two-region CryptaScreen stack (never production).

Needs CS_CONTRACT_US / CS_CONTRACT_EU / CS_CONTRACT_KEY_US / CS_CONTRACT_KEY_EU / CS_CONTRACT_KEY_RL; skipped when absent.
Data: the local stack's SYNTHETIC OFAC-SDN-shaped list only (positive-control address 0xc501...0001, listed name
"Synthia00003 QWERTYSON 00003"); clean addresses are well-formed placeholders. No real client data.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor

import pytest

from cryptascreen import (
    AuthenticationError,
    CryptaScreen,
    CryptaScreenError,
    RateLimitError,
    ValidationError,
)

URLS = {"us": os.environ.get("CS_CONTRACT_US"), "eu": os.environ.get("CS_CONTRACT_EU")}
KEYS = {"us": os.environ.get("CS_CONTRACT_KEY_US"), "eu": os.environ.get("CS_CONTRACT_KEY_EU")}

pytestmark = [
    pytest.mark.contract,
    pytest.mark.skipif(not all(URLS.values()), reason="no local stack (CS_CONTRACT_* not set)"),
]

LISTED = "0xc501000000000000000000000000000000000001"
CLEAN = "0x1111111111111111111111111111111111111111"
CLEAN2 = "0x2222222222222222222222222222222222222222"
LISTED_NAME = "Synthia00003 QWERTYSON 00003"


@pytest.fixture(params=["us", "eu"])
def region(request: pytest.FixtureRequest) -> str:
    return str(request.param)


@pytest.fixture
def client(region: str) -> Iterator[CryptaScreen]:
    with CryptaScreen(api_key=KEYS[region] or "", base_url=URLS[region], max_retries=0) as c:
        yield c


def test_listed_address_hits_the_seeded_entry(client: CryptaScreen) -> None:
    r = client.screening.screen_address({"address": LISTED, "chain": "ethereum"})
    assert r.sanctions_match is True
    assert r.risk_level == "CRITICAL"
    assert r.evaluation_id
    assert client.sanctions.check("ethereum", LISTED).match is True


def test_clean_address_has_no_match_in_checked_layers(client: CryptaScreen) -> None:
    r = client.screening.screen_address({"address": CLEAN, "chain": "ethereum"})
    assert r.sanctions_match is False
    assert r.risk_level != "CRITICAL"
    assert client.sanctions.check("ethereum", CLEAN).match is False


def test_history_evaluations_and_exposure_sections(client: CryptaScreen) -> None:
    r = client.screening.screen_address({"address": LISTED, "chain": "ethereum"})
    assert client.screening.get_history("ethereum", LISTED).address
    client.screening.list_evaluations("ethereum", LISTED, page=0, size=5)
    ev = client.screening.get_evaluation(r.evaluation_id or "")
    assert ev.evaluation_id == r.evaluation_id
    client.screening.get_exposure_paths("ethereum", LISTED, days=30)
    client.screening.get_counterparties("ethereum", LISTED, page=0, size=5)
    client.screening.get_transactions("ethereum", LISTED, page=0, size=5)


def test_sanctions_status(client: CryptaScreen) -> None:
    st = client.sanctions.get_status()
    assert st.total_active and st.total_active > 0


def test_bulk_sync_keeps_order(client: CryptaScreen) -> None:
    res = client.screening.screen_bulk(
        {"addresses": [LISTED, CLEAN, CLEAN2], "chains": ["ethereum"] * 3}
    )
    assert len(res) == 3
    assert [x.sanctions_match for x in res] == [True, False, False]


def test_bulk_async_job_completes_and_has_results(client: CryptaScreen) -> None:
    job = client.screening.screen_bulk_and_wait(
        {"addresses": [LISTED, CLEAN], "chains": ["ethereum"] * 2}, poll_interval=0.5, timeout=60
    )
    assert job.status in ("COMPLETED", "PARTIAL")
    page = client.screening.get_job_results(job.job_id or "", page=0, size=10)
    assert page.total_items == 2 and len(page.items) == 2
    assert any(j.job_id == job.job_id for j in client.screening.list_jobs())


def test_name_screening_listed_and_clean(client: CryptaScreen) -> None:
    hit = client.names.screen({"name": LISTED_NAME, "type": "PERSON"})
    assert hit.outcome in ("REVIEW", "CONFIRMED_MATCH")
    clean = client.names.screen({"name": "Unrelated Person Zq-contract", "type": "PERSON"})
    assert clean.outcome == "CLEAR"
    assert client.names.get(hit.screening_id or "").screening_id == hit.screening_id
    assert any(x.screening_id == hit.screening_id for x in client.names.history(limit=20))


# ---- error cases --------------------------------------------------------------------------------------------------


def test_401_wrong_key(region: str) -> None:
    bad = "csk_" + region + "_ffffffffffffffffffffffffffffffff"
    with (
        CryptaScreen(api_key=bad, base_url=URLS[region], max_retries=0) as c,
        pytest.raises(AuthenticationError) as ei,
    ):
        c.sanctions.get_status()
    assert ei.value.status == 401


def test_400_unknown_chain_and_bad_address(client: CryptaScreen) -> None:
    with pytest.raises(ValidationError) as ei:
        client.screening.screen_address({"address": LISTED, "chain": "no-such-chain"})
    assert ei.value.status == 400 and ei.value.validation_code == "UNKNOWN_CHAIN"
    with pytest.raises(ValidationError) as ei2:
        client.screening.screen_address({"address": "0x123", "chain": "ethereum"})
    assert ei2.value.validation_code in ("INVALID_ADDRESS_FORMAT", "INVALID_CHECKSUM")


def test_400_bulk_reports_every_invalid_item(client: CryptaScreen) -> None:
    with pytest.raises(ValidationError) as ei:
        client.screening.screen_bulk(
            {"addresses": [CLEAN, "0xbad", "0xbad2"], "chains": ["ethereum"] * 3}
        )
    assert ei.value.validation_code == "INVALID_BULK_ITEMS"
    assert len(ei.value.items) == 2
    assert {"address[1]", "address[2]"} <= set(
        ei.value.field_errors
    )  # bulk item keys use the item field name: address[i]


def test_unknown_job_is_a_typed_error(client: CryptaScreen) -> None:
    with pytest.raises(CryptaScreenError) as ei:
        client.screening.poll_job("00000000-0000-4000-8000-000000000000")
    assert ei.value.status in (400, 404)


def test_429_rate_limit_is_raised_after_the_key_budget_is_used() -> None:
    """A dedicated key is hammered until the per-key limiter answers 429 (retries off): RateLimitError."""
    key = os.environ.get("CS_CONTRACT_KEY_RL") or ""
    base = URLS["us"]

    def one(_: int) -> str:
        with CryptaScreen(api_key=key, base_url=base, max_retries=0, timeout=30) as c:
            try:
                c.sanctions.get_status()
            except RateLimitError as e:
                assert e.status == 429 and e.code == "RATE_LIMIT_EXCEEDED"
                return "429"
            return "ok"

    with ThreadPoolExecutor(16) as pool:
        outcomes = list(pool.map(one, range(1300)))
    assert "429" in outcomes, f"no 429 after {len(outcomes)} requests: {set(outcomes)}"


def test_webhook_endpoints_are_readable_with_an_api_key(client: CryptaScreen) -> None:
    assert isinstance(client.webhooks.list(), list)
