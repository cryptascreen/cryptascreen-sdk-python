# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Behaviour of the account / capabilities / settings / monitoring resources (sync + async) and the webhook read models."""

from __future__ import annotations

import json

import httpx
import pytest

from cryptascreen import AsyncCryptaScreen, CryptaScreenError
from cryptascreen.types import (
    AuthMe,
    BreachDetection,
    BreachSummary,
    Capabilities,
    MonitoredWallet,
    MonitoringOverview,
    ScoreThresholdAuditPage,
    ScoreThresholdSettings,
    VendorKeyView,
    WebhookConfig,
    WebhookDelivery,
)

from .conftest import TEST_ADDRESS, Recorder, make_client


def test_auth_me_and_capabilities_are_typed() -> None:
    r = Recorder(
        [
            httpx.Response(
                200,
                json={
                    "email": "a@example.test",
                    "authMethod": "API_KEY",
                    "tenantId": "9",
                    "tier": "PROFESSIONAL",
                },
            ),
            httpx.Response(
                200,
                json={
                    "chains": [
                        {
                            "chain": "ethereum",
                            "displayName": "Ethereum",
                            "onChain": "COVERED",
                            "sanctionsScreenable": True,
                        }
                    ],
                    "layers": [
                        {
                            "layer": "SANCTIONS",
                            "state": "ON",
                            "status": "COMPLETE",
                            "sources": ["OFAC_SDN"],
                        }
                    ],
                },
            ),
        ]
    )
    c = make_client(r)
    me = c.auth.me()
    assert isinstance(me, AuthMe) and me.auth_method == "API_KEY" and me.tenant_id == "9"
    caps = c.capabilities.get()
    assert isinstance(caps, Capabilities)
    assert (
        caps.chains
        and caps.chains[0].on_chain == "COVERED"
        and caps.layers
        and caps.layers[0].sources == ["OFAC_SDN"]
    )
    assert r.calls == ["GET /api/v1/auth/me", "GET /api/v1/capabilities"]


def test_settings_reads_and_limit_query() -> None:
    r = Recorder(
        [
            httpx.Response(
                200,
                json={
                    "reviewAt": 40,
                    "blockAt": 70,
                    "source": "DEFAULT",
                    "defaults": {"reviewAt": 40, "blockAt": 70},
                },
            ),
            httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "actor": "user:1",
                            "action": "SET",
                            "current": {"reviewAt": 30, "blockAt": 60},
                        }
                    ]
                },
            ),
            httpx.Response(200, json={"items": []}),
            httpx.Response(
                200, json=[{"vendor": "CHAINALYSIS", "configured": False, "last4": None}]
            ),
        ]
    )
    c = make_client(r)
    t = c.settings.get_score_thresholds()
    assert (
        isinstance(t, ScoreThresholdSettings)
        and (t.review_at, t.block_at) == (40, 70)
        and t.defaults is not None
    )
    page = c.settings.get_score_threshold_audit(limit=5)
    assert isinstance(page, ScoreThresholdAuditPage) and page.items[0].action == "SET"
    assert r.requests[1].url.params["limit"] == "5"
    c.settings.get_name_list_audit()
    assert "limit" not in r.requests[2].url.params
    keys = c.settings.list_vendor_keys()
    assert isinstance(keys[0], VendorKeyView) and keys[0].vendor == "CHAINALYSIS"


def test_monitoring_wallet_name_and_breach_calls() -> None:
    r = Recorder(
        [
            httpx.Response(
                200, json={"id": 3, "address": TEST_ADDRESS, "chain": "ethereum", "label": "t"}
            ),
            httpx.Response(200, json={"deleted": True}),
            httpx.Response(201, json={"id": 5}),
            httpx.Response(200, json={"removed": True}),
            httpx.Response(200, json={"names": [], "wallets": [], "nameHits": [{"item_id": 1}]}),
            httpx.Response(200, json=[{"id": 1, "severity": "HIGH"}]),
            httpx.Response(
                200, json={"unacknowledgedCount": 2, "bySeverity": {"HIGH": 2}, "totalBreaches": 2}
            ),
            httpx.Response(200, json={"id": 1, "acknowledgedAt": "2026-11-23T00:00:00Z"}),
        ]
    )
    c = make_client(r)
    w = c.monitoring.add_wallet({"address": TEST_ADDRESS, "chain": "ethereum", "label": "t"})
    assert isinstance(w, MonitoredWallet) and w.id == 3
    assert json.loads(r.requests[0].content) == {
        "address": TEST_ADDRESS,
        "chain": "ethereum",
        "label": "t",
    }
    assert c.monitoring.remove_wallet(3).deleted is True
    c.monitoring.add_name({"name": "Test Name", "dateOfBirth": "1970-01-01"})
    assert json.loads(r.requests[2].content) == {"name": "Test Name", "dateOfBirth": "1970-01-01"}
    assert c.monitoring.remove_name(5).removed is True
    ov = c.monitoring.get_overview()
    assert isinstance(ov, MonitoringOverview) and ov.name_hits == [{"item_id": 1}]
    assert isinstance(c.monitoring.list_breaches()[0], BreachDetection)
    s = c.monitoring.get_breach_summary()
    assert isinstance(s, BreachSummary) and s.by_severity == {"HIGH": 2}
    assert c.monitoring.acknowledge_breach(1).acknowledged_at
    assert r.calls == [
        "POST /api/v1/monitoring/wallets",
        "DELETE /api/v1/monitoring/wallets/3",
        "POST /api/v1/monitoring/names",
        "DELETE /api/v1/monitoring/names/5",
        "GET /api/v1/monitoring/overview",
        "GET /api/v1/monitoring/breaches",
        "GET /api/v1/monitoring/breaches/summary",
        "POST /api/v1/monitoring/breaches/1/acknowledge",
    ]


def test_id_is_url_encoded_and_a_duplicate_wallet_is_a_validation_error() -> None:
    r = Recorder(
        [
            httpx.Response(
                400, json={"error": "DUPLICATE", "message": "Wallet is already being monitored"}
            )
        ]
    )
    c = make_client(r)
    with pytest.raises(CryptaScreenError) as ei:
        c.monitoring.add_wallet({"address": TEST_ADDRESS, "chain": "ethereum"})
    assert ei.value.status == 400
    r2 = Recorder([httpx.Response(200, json={})])
    make_client(r2).monitoring.remove_wallet("a/b")
    assert r2.last.url.raw_path.decode().endswith("/wallets/a%2Fb")


def test_webhook_read_models_match_the_api() -> None:
    r = Recorder(
        [
            httpx.Response(
                200,
                json=[
                    {
                        "id": 1,
                        "url": "https://example.test/h",
                        "secret": "whsec_…ab12",
                        "events": ["CRITICAL"],
                        "isActive": True,
                        "description": "d",
                        "createdAt": "2026-11-23T00:00:00Z",
                    }
                ],
            ),
            httpx.Response(
                200,
                json=[
                    {
                        "id": "6f0c1c2e-0000-4000-8000-000000000001",
                        "webhookConfigId": 1,
                        "eventType": "CRITICAL",
                        "status": "DELIVERED",
                        "attemptCount": 1,
                        "responseCode": 204,
                    }
                ],
            ),
        ]
    )
    c = make_client(r)
    hooks = c.webhooks.list()
    assert isinstance(hooks[0], WebhookConfig) and hooks[0].is_active is True and hooks[0].id == 1
    d = c.webhooks.get_deliveries(hooks[0].id)
    assert (
        isinstance(d[0], WebhookDelivery)
        and d[0].status == "DELIVERED"
        and d[0].response_code == 204
    )
    assert r.last.url.path == "/api/v1/webhooks/1/deliveries" and not r.last.url.params


@pytest.mark.asyncio
async def test_async_variants_hit_the_same_operations() -> None:
    r = Recorder([httpx.Response(200, json={})])
    c = AsyncCryptaScreen(api_key="csk_test", base_url="https://api.example.test")
    from cryptascreen.client import AsyncHttpClient

    await c._http.close()
    c._http = AsyncHttpClient(c._config, transport=httpx.MockTransport(r))
    for name in ("auth", "capabilities", "settings", "monitoring"):
        res = getattr(c, name)
        res._http = c._http
    await c.auth.me()
    await c.capabilities.get()
    await c.settings.get_name_matching_audit(limit=3)
    await c.monitoring.acknowledge_breach(4)
    assert r.calls == [
        "GET /api/v1/auth/me",
        "GET /api/v1/capabilities",
        "GET /api/v1/settings/name-matching/audit",
        "POST /api/v1/monitoring/breaches/4/acknowledge",
    ]
    assert r.requests[2].url.params["limit"] == "3"
    await c.close()
