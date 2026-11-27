# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Shared test fixtures for the CryptaScreen SDK test suite."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx
import pytest

from cryptascreen import CryptaScreen
from cryptascreen.client import HttpClient
from cryptascreen.config import Config

FIXTURES = Path(__file__).parent / "fixtures"
# Test-only address (documented EVM test address; no client data).
TEST_ADDRESS = "0x" + "ab" * 20


def load_fixture(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class Recorder:
    """httpx MockTransport handler that records requests and plays scripted responses."""

    def __init__(
        self,
        responses: list[httpx.Response] | Callable[[httpx.Request], httpx.Response] | None = None,
    ) -> None:
        self.requests: list[httpx.Request] = []
        self._responses = responses if responses is not None else [httpx.Response(200, json={})]

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if callable(self._responses):
            return self._responses(request)
        idx = min(len(self.requests) - 1, len(self._responses) - 1)
        return self._responses[idx]

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    @property
    def calls(self) -> list[str]:
        return [f"{r.method} {r.url.path}" for r in self.requests]


def make_client(recorder: Recorder, **kw: Any) -> CryptaScreen:
    """A CryptaScreen client backed by the recorder (no sleeping between retries)."""
    cfg: dict[str, Any] = {"retry_base_delay": 0.0}
    cfg.update(kw)
    client = CryptaScreen.__new__(CryptaScreen)
    config = Config(
        api_key="csk_test",
        base_url="https://api.example.test",
        max_retries=cfg.pop("max_retries", 3),
        retry_base_delay=cfg.pop("retry_base_delay"),
    )
    client._config = config
    client._http = HttpClient(config, transport=httpx.MockTransport(recorder))
    from cryptascreen.client import (
        AlertsResource,
        AuthResource,
        CapabilitiesResource,
        CasesResource,
        ComplianceResource,
        GraphResource,
        IntelligenceResource,
        MonitoringResource,
        NamesResource,
        SanctionsResource,
        ScreeningResource,
        SettingsResource,
        WebhooksResource,
    )

    for name, cls in [
        ("screening", ScreeningResource),
        ("sanctions", SanctionsResource),
        ("names", NamesResource),
        ("graph", GraphResource),
        ("cases", CasesResource),
        ("alerts", AlertsResource),
        ("compliance", ComplianceResource),
        ("intelligence", IntelligenceResource),
        ("webhooks", WebhooksResource),
        ("auth", AuthResource),
        ("capabilities", CapabilitiesResource),
        ("settings", SettingsResource),
        ("monitoring", MonitoringResource),
    ]:
        setattr(client, name, cls(client._http))
    return client


@pytest.fixture
def recorder() -> Recorder:
    return Recorder()
