# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Chains and layers (resource ``client.capabilities``)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cryptascreen.types._account import (
    Capabilities,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class CapabilitiesResource:
    """Synchronous chains and layers. Access via ``client.capabilities``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self) -> Capabilities:
        """Chains the screening API accepts (on-chain COVERED / UNAVAILABLE) and the live layer state (ON / OFF)."""
        data = self._http.request("GET", "/api/v1/capabilities")
        return Capabilities.model_validate(data)


class AsyncCapabilitiesResource:
    """Asynchronous chains and layers. Access via ``client.capabilities``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> Capabilities:
        """Chains the screening API accepts (on-chain COVERED / UNAVAILABLE) and the live layer state (ON / OFF)."""
        data = await self._http.request("GET", "/api/v1/capabilities")
        return Capabilities.model_validate(data)
