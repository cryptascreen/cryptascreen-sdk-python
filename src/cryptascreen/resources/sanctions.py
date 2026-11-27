# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Sanctions resource (mirrors @cryptascreen/sdk sanctions endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cryptascreen._util import _enc
from cryptascreen.types._models import (
    SanctionsCheckResponse,
    SanctionsStatusResponse,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class SanctionsResource:
    """Synchronous sanctions operations. Access via ``client.sanctions``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def check(self, chain: str, address: str) -> SanctionsCheckResponse:
        """GET /sanctions/check/{chain}/{address}"""
        data = self._http.request("GET", f"/api/v1/sanctions/check/{_enc(chain)}/{_enc(address)}")
        return SanctionsCheckResponse.model_validate(data)

    def get_status(self) -> SanctionsStatusResponse:
        """GET /sanctions/status"""
        data = self._http.request("GET", "/api/v1/sanctions/status")
        return SanctionsStatusResponse.model_validate(data)


class AsyncSanctionsResource:
    """Asynchronous sanctions operations. Access via ``client.sanctions``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def check(self, chain: str, address: str) -> SanctionsCheckResponse:
        """GET /sanctions/check/{chain}/{address}"""
        data = await self._http.request(
            "GET", f"/api/v1/sanctions/check/{_enc(chain)}/{_enc(address)}"
        )
        return SanctionsCheckResponse.model_validate(data)

    async def get_status(self) -> SanctionsStatusResponse:
        """GET /sanctions/status"""
        data = await self._http.request("GET", "/api/v1/sanctions/status")
        return SanctionsStatusResponse.model_validate(data)
