"""Read access to the tenant settings (resource ``client.settings``)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cryptascreen._util import _query
from cryptascreen.types._account import (
    ItemsResponse,
    NameMatchingStrength,
    ScoreThresholdAuditPage,
    ScoreThresholdSettings,
    VendorKeyView,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class SettingsResource:
    """Synchronous read access to the tenant settings. Access via ``client.settings``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_score_thresholds(self) -> ScoreThresholdSettings:
        """Review / block thresholds of the calling tenant (defaults 40 / 70 until changed; paid plans)."""
        data = self._http.request("GET", "/api/v1/settings/score-thresholds")
        return ScoreThresholdSettings.model_validate(data)

    def get_score_threshold_audit(self, *, limit: int | None = None) -> ScoreThresholdAuditPage:
        """Change history of the thresholds, newest first."""
        data = self._http.request(
            "GET", "/api/v1/settings/score-thresholds/audit", params=_query(limit=limit)
        )
        return ScoreThresholdAuditPage.model_validate(data)

    def get_name_matching(self) -> NameMatchingStrength:
        """Name-matching strength of the calling tenant (default CONSERVATIVE; paid plans)."""
        data = self._http.request("GET", "/api/v1/settings/name-matching")
        return NameMatchingStrength.model_validate(data)

    def get_name_matching_audit(self, *, limit: int | None = None) -> ItemsResponse:
        """Change history of the matching strength, newest first."""
        data = self._http.request(
            "GET", "/api/v1/settings/name-matching/audit", params=_query(limit=limit)
        )
        return ItemsResponse.model_validate(data)

    def get_name_lists(self) -> ItemsResponse:
        """Allow / block list entries of the calling tenant (exact identifiers, applied before fuzzy matching)."""
        data = self._http.request("GET", "/api/v1/settings/name-lists")
        return ItemsResponse.model_validate(data)

    def get_name_list_audit(self, *, limit: int | None = None) -> ItemsResponse:
        """Audit of allow / block entries (added, removed, applied), newest first."""
        data = self._http.request(
            "GET", "/api/v1/settings/name-lists/audit", params=_query(limit=limit)
        )
        return ItemsResponse.model_validate(data)

    def list_vendor_keys(self) -> list[VendorKeyView]:
        """The vendors with their configured state (last4 and fingerprint only; never the key)."""
        data = self._http.request("GET", "/api/v1/settings/vendor-keys")
        return [VendorKeyView.model_validate(x) for x in data]


class AsyncSettingsResource:
    """Asynchronous read access to the tenant settings. Access via ``client.settings``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_score_thresholds(self) -> ScoreThresholdSettings:
        """Review / block thresholds of the calling tenant (defaults 40 / 70 until changed; paid plans)."""
        data = await self._http.request("GET", "/api/v1/settings/score-thresholds")
        return ScoreThresholdSettings.model_validate(data)

    async def get_score_threshold_audit(
        self, *, limit: int | None = None
    ) -> ScoreThresholdAuditPage:
        """Change history of the thresholds, newest first."""
        data = await self._http.request(
            "GET", "/api/v1/settings/score-thresholds/audit", params=_query(limit=limit)
        )
        return ScoreThresholdAuditPage.model_validate(data)

    async def get_name_matching(self) -> NameMatchingStrength:
        """Name-matching strength of the calling tenant (default CONSERVATIVE; paid plans)."""
        data = await self._http.request("GET", "/api/v1/settings/name-matching")
        return NameMatchingStrength.model_validate(data)

    async def get_name_matching_audit(self, *, limit: int | None = None) -> ItemsResponse:
        """Change history of the matching strength, newest first."""
        data = await self._http.request(
            "GET", "/api/v1/settings/name-matching/audit", params=_query(limit=limit)
        )
        return ItemsResponse.model_validate(data)

    async def get_name_lists(self) -> ItemsResponse:
        """Allow / block list entries of the calling tenant (exact identifiers, applied before fuzzy matching)."""
        data = await self._http.request("GET", "/api/v1/settings/name-lists")
        return ItemsResponse.model_validate(data)

    async def get_name_list_audit(self, *, limit: int | None = None) -> ItemsResponse:
        """Audit of allow / block entries (added, removed, applied), newest first."""
        data = await self._http.request(
            "GET", "/api/v1/settings/name-lists/audit", params=_query(limit=limit)
        )
        return ItemsResponse.model_validate(data)

    async def list_vendor_keys(self) -> list[VendorKeyView]:
        """The vendors with their configured state (last4 and fingerprint only; never the key)."""
        data = await self._http.request("GET", "/api/v1/settings/vendor-keys")
        return [VendorKeyView.model_validate(x) for x in data]
