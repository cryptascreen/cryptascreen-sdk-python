# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Graph resource (mirrors @cryptascreen/sdk graph endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptascreen._util import _body
from cryptascreen.types._models import (
    GraphRequest,
    GraphResponse,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class GraphResource:
    """Synchronous graph operations. Access via ``client.graph``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def build_graph(self, request: GraphRequest | dict[str, Any]) -> GraphResponse:
        """POST /investigate/graph"""
        data = self._http.request("POST", "/api/v1/investigate/graph", json=_body(request))
        return GraphResponse.model_validate(data)

    def export_graph(self, request: GraphRequest | dict[str, Any], *, format: str = "json") -> Any:
        """Export a flow-of-funds graph: parsed JSON for ``json``, raw bytes for ``csv``."""
        return self._http.request(
            "POST",
            "/api/v1/investigate/graph/export",
            json=_body(request),
            params={"format": format},
            binary=format != "json",
        )

    def trace(self, request: GraphRequest | dict[str, Any]) -> GraphResponse:
        """POST /investigate/trace"""
        data = self._http.request("POST", "/api/v1/investigate/trace", json=_body(request))
        return GraphResponse.model_validate(data)


class AsyncGraphResource:
    """Asynchronous graph operations. Access via ``client.graph``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def build_graph(self, request: GraphRequest | dict[str, Any]) -> GraphResponse:
        """POST /investigate/graph"""
        data = await self._http.request("POST", "/api/v1/investigate/graph", json=_body(request))
        return GraphResponse.model_validate(data)

    async def export_graph(
        self, request: GraphRequest | dict[str, Any], *, format: str = "json"
    ) -> Any:
        """Export a flow-of-funds graph: parsed JSON for ``json``, raw bytes for ``csv``."""
        return await self._http.request(
            "POST",
            "/api/v1/investigate/graph/export",
            json=_body(request),
            params={"format": format},
            binary=format != "json",
        )

    async def trace(self, request: GraphRequest | dict[str, Any]) -> GraphResponse:
        """POST /investigate/trace"""
        data = await self._http.request("POST", "/api/v1/investigate/trace", json=_body(request))
        return GraphResponse.model_validate(data)
