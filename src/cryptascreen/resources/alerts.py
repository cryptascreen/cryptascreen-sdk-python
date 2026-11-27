# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Alerts resource (mirrors @cryptascreen/sdk alerts endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cryptascreen._util import _enc
from cryptascreen.types._models import (
    AlertDetail,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class AlertsResource:
    """Synchronous alerts operations. Access via ``client.alerts``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, id: str) -> AlertDetail:
        """GET /alerts/{id}"""
        data = self._http.request("GET", f"/api/v1/alerts/{_enc(id)}")
        return AlertDetail.model_validate(data)

    def acknowledge(self, id: int | str, note: str | None = None) -> AlertDetail:
        """Acknowledge an alert. Idempotent: a repeat returns the stored acknowledgement with alreadyAcknowledged true."""
        body = {"note": note.strip()} if note and note.strip() else {}
        data = self._http.request("POST", f"/api/v1/alerts/{_enc(str(id))}/acknowledge", json=body)
        return AlertDetail.model_validate(data)


class AsyncAlertsResource:
    """Asynchronous alerts operations. Access via ``client.alerts``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self, id: str) -> AlertDetail:
        """GET /alerts/{id}"""
        data = await self._http.request("GET", f"/api/v1/alerts/{_enc(id)}")
        return AlertDetail.model_validate(data)

    async def acknowledge(self, id: int | str, note: str | None = None) -> AlertDetail:
        """Acknowledge an alert. Idempotent: a repeat returns the stored acknowledgement with alreadyAcknowledged true."""
        body = {"note": note.strip()} if note and note.strip() else {}
        data = await self._http.request(
            "POST", f"/api/v1/alerts/{_enc(str(id))}/acknowledge", json=body
        )
        return AlertDetail.model_validate(data)
