"""Wallet / name monitoring and breach detections (resource ``client.monitoring``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptascreen._util import _body, _enc
from cryptascreen.types._account import (
    AddMonitoredWalletRequest,
    BreachDetection,
    BreachSummary,
    DeletedResponse,
    MonitoredName,
    MonitoredNamesResponse,
    MonitoredWallet,
    MonitoringOverview,
    RemovedResponse,
)
from cryptascreen.types._models import NameScreenRequest

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class MonitoringResource:
    """Synchronous wallet / name monitoring and breach detections. Access via ``client.monitoring``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_wallets(self) -> list[MonitoredWallet]:
        """Monitored wallets of the calling tenant."""
        data = self._http.request("GET", "/api/v1/monitoring/wallets")
        return [MonitoredWallet.model_validate(x) for x in data]

    def add_wallet(self, request: AddMonitoredWalletRequest | dict[str, Any]) -> MonitoredWallet:
        """Add a wallet to monitoring (plan-limited; a duplicate is a 400 DUPLICATE)."""
        data = self._http.request("POST", "/api/v1/monitoring/wallets", json=_body(request))
        return MonitoredWallet.model_validate(data)

    def remove_wallet(self, id: int | str) -> DeletedResponse:
        """Remove a wallet from monitoring."""
        data = self._http.request("DELETE", f"/api/v1/monitoring/wallets/{_enc(str(id))}")
        return DeletedResponse.model_validate(data)

    def list_names(self) -> MonitoredNamesResponse:
        """Monitored names of the calling tenant and how many the plan has used."""
        data = self._http.request("GET", "/api/v1/monitoring/names")
        return MonitoredNamesResponse.model_validate(data)

    def add_name(self, request: NameScreenRequest | dict[str, Any]) -> MonitoredName:
        """Save a name to the monitored list (plan-limited like monitored wallets)."""
        data = self._http.request("POST", "/api/v1/monitoring/names", json=_body(request))
        return MonitoredName.model_validate(data)

    def remove_name(self, id: int | str) -> RemovedResponse:
        """Remove a name from the monitored list."""
        data = self._http.request("DELETE", f"/api/v1/monitoring/names/{_enc(str(id))}")
        return RemovedResponse.model_validate(data)

    def get_overview(self) -> MonitoringOverview:
        """Names and wallets on the monitored list, with the last known hits of each name."""
        data = self._http.request("GET", "/api/v1/monitoring/overview")
        return MonitoringOverview.model_validate(data)

    def list_breaches(self) -> list[BreachDetection]:
        """All breach detections of the calling tenant, newest first."""
        data = self._http.request("GET", "/api/v1/monitoring/breaches")
        return [BreachDetection.model_validate(x) for x in data]

    def get_breach_summary(self) -> BreachSummary:
        """Counts of breach detections (unacknowledged, by severity, total)."""
        data = self._http.request("GET", "/api/v1/monitoring/breaches/summary")
        return BreachSummary.model_validate(data)

    def acknowledge_breach(self, id: int | str) -> BreachDetection:
        """Acknowledge a breach detection (a second acknowledge is a 400 ALREADY_ACKNOWLEDGED)."""
        data = self._http.request(
            "POST", f"/api/v1/monitoring/breaches/{_enc(str(id))}/acknowledge"
        )
        return BreachDetection.model_validate(data)


class AsyncMonitoringResource:
    """Asynchronous wallet / name monitoring and breach detections. Access via ``client.monitoring``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_wallets(self) -> list[MonitoredWallet]:
        """Monitored wallets of the calling tenant."""
        data = await self._http.request("GET", "/api/v1/monitoring/wallets")
        return [MonitoredWallet.model_validate(x) for x in data]

    async def add_wallet(
        self, request: AddMonitoredWalletRequest | dict[str, Any]
    ) -> MonitoredWallet:
        """Add a wallet to monitoring (plan-limited; a duplicate is a 400 DUPLICATE)."""
        data = await self._http.request("POST", "/api/v1/monitoring/wallets", json=_body(request))
        return MonitoredWallet.model_validate(data)

    async def remove_wallet(self, id: int | str) -> DeletedResponse:
        """Remove a wallet from monitoring."""
        data = await self._http.request("DELETE", f"/api/v1/monitoring/wallets/{_enc(str(id))}")
        return DeletedResponse.model_validate(data)

    async def list_names(self) -> MonitoredNamesResponse:
        """Monitored names of the calling tenant and how many the plan has used."""
        data = await self._http.request("GET", "/api/v1/monitoring/names")
        return MonitoredNamesResponse.model_validate(data)

    async def add_name(self, request: NameScreenRequest | dict[str, Any]) -> MonitoredName:
        """Save a name to the monitored list (plan-limited like monitored wallets)."""
        data = await self._http.request("POST", "/api/v1/monitoring/names", json=_body(request))
        return MonitoredName.model_validate(data)

    async def remove_name(self, id: int | str) -> RemovedResponse:
        """Remove a name from the monitored list."""
        data = await self._http.request("DELETE", f"/api/v1/monitoring/names/{_enc(str(id))}")
        return RemovedResponse.model_validate(data)

    async def get_overview(self) -> MonitoringOverview:
        """Names and wallets on the monitored list, with the last known hits of each name."""
        data = await self._http.request("GET", "/api/v1/monitoring/overview")
        return MonitoringOverview.model_validate(data)

    async def list_breaches(self) -> list[BreachDetection]:
        """All breach detections of the calling tenant, newest first."""
        data = await self._http.request("GET", "/api/v1/monitoring/breaches")
        return [BreachDetection.model_validate(x) for x in data]

    async def get_breach_summary(self) -> BreachSummary:
        """Counts of breach detections (unacknowledged, by severity, total)."""
        data = await self._http.request("GET", "/api/v1/monitoring/breaches/summary")
        return BreachSummary.model_validate(data)

    async def acknowledge_breach(self, id: int | str) -> BreachDetection:
        """Acknowledge a breach detection (a second acknowledge is a 400 ALREADY_ACKNOWLEDGED)."""
        data = await self._http.request(
            "POST", f"/api/v1/monitoring/breaches/{_enc(str(id))}/acknowledge"
        )
        return BreachDetection.model_validate(data)
