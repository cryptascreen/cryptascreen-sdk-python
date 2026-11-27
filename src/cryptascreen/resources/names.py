# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Names resource (mirrors @cryptascreen/sdk names endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptascreen._util import _body, _enc, _query
from cryptascreen.types._models import (
    NameDecisionRequest,
    NameMatchDecision,
    NameScreeningHistoryItem,
    NameScreenRequest,
    NameScreenResponse,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class NamesResource:
    """Synchronous names operations. Access via ``client.names``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def screen(
        self, request: NameScreenRequest | dict[str, Any], *, idempotency_key: str | None = None
    ) -> NameScreenResponse:
        """Screen one name. An invalid request is a 400 (ValidationError) and is not counted."""
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        data = self._http.request(
            "POST", "/api/v1/screen/name", json=_body(request), headers=headers
        )
        return NameScreenResponse.model_validate(data)

    def get(self, screening_id: str) -> NameScreenResponse:
        """GET /screen/name/{screeningId}"""
        data = self._http.request("GET", f"/api/v1/screen/name/{_enc(screening_id)}")
        return NameScreenResponse.model_validate(data)

    def history(self, *, limit: int = 50) -> list[NameScreeningHistoryItem]:
        """GET /screen/name/history"""
        data = self._http.request("GET", "/api/v1/screen/name/history", params=_query(limit=limit))
        return [NameScreeningHistoryItem.model_validate(x) for x in data]

    def decide(self, request: NameDecisionRequest | dict[str, Any]) -> NameMatchDecision:
        """POST /screen/name/decisions"""
        data = self._http.request("POST", "/api/v1/screen/name/decisions", json=_body(request))
        return NameMatchDecision.model_validate(data)

    def decision_audit(self, *, format: str = "json") -> Any:
        """GET /screen/name/decisions/audit"""
        return self._http.request(
            "GET", "/api/v1/screen/name/decisions/audit", params=_query(format=format)
        )


class AsyncNamesResource:
    """Asynchronous names operations. Access via ``client.names``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def screen(
        self, request: NameScreenRequest | dict[str, Any], *, idempotency_key: str | None = None
    ) -> NameScreenResponse:
        """Screen one name. An invalid request is a 400 (ValidationError) and is not counted."""
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        data = await self._http.request(
            "POST", "/api/v1/screen/name", json=_body(request), headers=headers
        )
        return NameScreenResponse.model_validate(data)

    async def get(self, screening_id: str) -> NameScreenResponse:
        """GET /screen/name/{screeningId}"""
        data = await self._http.request("GET", f"/api/v1/screen/name/{_enc(screening_id)}")
        return NameScreenResponse.model_validate(data)

    async def history(self, *, limit: int = 50) -> list[NameScreeningHistoryItem]:
        """GET /screen/name/history"""
        data = await self._http.request(
            "GET", "/api/v1/screen/name/history", params=_query(limit=limit)
        )
        return [NameScreeningHistoryItem.model_validate(x) for x in data]

    async def decide(self, request: NameDecisionRequest | dict[str, Any]) -> NameMatchDecision:
        """POST /screen/name/decisions"""
        data = await self._http.request(
            "POST", "/api/v1/screen/name/decisions", json=_body(request)
        )
        return NameMatchDecision.model_validate(data)

    async def decision_audit(self, *, format: str = "json") -> Any:
        """GET /screen/name/decisions/audit"""
        return await self._http.request(
            "GET", "/api/v1/screen/name/decisions/audit", params=_query(format=format)
        )
