# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Intelligence resource (mirrors @cryptascreen/sdk intelligence endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cryptascreen._util import _enc
from cryptascreen.errors import CryptaScreenError
from cryptascreen.types._models import (
    EntityLabel,
    VaspInfo,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class IntelligenceResource:
    """Synchronous intelligence operations. Access via ``client.intelligence``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_entity_labels(self, chain: str, address: str) -> list[EntityLabel]:
        """All entity attributions for an address (empty list = no label known; NOT a clean verdict)."""
        data = self._http.request(
            "GET", f"/api/v1/intelligence/entity/{_enc(chain)}/{_enc(address)}"
        )
        return [EntityLabel.model_validate(x) for x in data] if isinstance(data, list) else []

    def get_entity_label(self, address: str, chain: str) -> EntityLabel | None:
        """Deprecated: first entity attribution or None; use get_entity_labels."""
        labels = self.get_entity_labels(chain, address)
        return labels[0] if labels else None

    def get_vasp_info(self, vasp_id: str) -> VaspInfo:
        """Deprecated: there is no VASP profile endpoint; raises without making a request."""
        raise CryptaScreenError(
            f"get_vasp_info({vasp_id}) is not available: the API has no VASP profile endpoint. Use compliance.identify_vasp(chain, address).",
            0,
            "ENDPOINT_NOT_AVAILABLE",
        )


class AsyncIntelligenceResource:
    """Asynchronous intelligence operations. Access via ``client.intelligence``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_entity_labels(self, chain: str, address: str) -> list[EntityLabel]:
        """All entity attributions for an address (empty list = no label known; NOT a clean verdict)."""
        data = await self._http.request(
            "GET", f"/api/v1/intelligence/entity/{_enc(chain)}/{_enc(address)}"
        )
        return [EntityLabel.model_validate(x) for x in data] if isinstance(data, list) else []

    async def get_entity_label(self, address: str, chain: str) -> EntityLabel | None:
        """Deprecated: first entity attribution or None; use get_entity_labels."""
        labels = await self.get_entity_labels(chain, address)
        return labels[0] if labels else None

    async def get_vasp_info(self, vasp_id: str) -> VaspInfo:
        """Deprecated: there is no VASP profile endpoint; raises without making a request."""
        raise CryptaScreenError(
            f"get_vasp_info({vasp_id}) is not available: the API has no VASP profile endpoint. Use compliance.identify_vasp(chain, address).",
            0,
            "ENDPOINT_NOT_AVAILABLE",
        )
