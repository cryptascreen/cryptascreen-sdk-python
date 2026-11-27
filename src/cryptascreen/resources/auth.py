# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Caller identity (resource ``client.auth``)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cryptascreen.types._account import (
    AuthMe,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class AuthResource:
    """Synchronous caller identity. Access via ``client.auth``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def me(self) -> AuthMe:
        """The calling identity. With an API key this is the key's tenant owner (authMethod API_KEY)."""
        data = self._http.request("GET", "/api/v1/auth/me")
        return AuthMe.model_validate(data)


class AsyncAuthResource:
    """Asynchronous caller identity. Access via ``client.auth``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def me(self) -> AuthMe:
        """The calling identity. With an API key this is the key's tenant owner (authMethod API_KEY)."""
        data = await self._http.request("GET", "/api/v1/auth/me")
        return AuthMe.model_validate(data)
