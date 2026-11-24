"""Main CryptaScreen SDK client - sync and async."""

from __future__ import annotations

from types import TracebackType
from typing import Any

import httpx

from cryptascreen.config import Config, resolve_base_url
from cryptascreen.resources.alerts import AlertsResource, AsyncAlertsResource
from cryptascreen.resources.auth import AsyncAuthResource, AuthResource
from cryptascreen.resources.capabilities import AsyncCapabilitiesResource, CapabilitiesResource
from cryptascreen.resources.cases import AsyncCasesResource, CasesResource
from cryptascreen.resources.compliance import AsyncComplianceResource, ComplianceResource
from cryptascreen.resources.graph import AsyncGraphResource, GraphResource
from cryptascreen.resources.intelligence import AsyncIntelligenceResource, IntelligenceResource
from cryptascreen.resources.monitoring import AsyncMonitoringResource, MonitoringResource
from cryptascreen.resources.names import AsyncNamesResource, NamesResource
from cryptascreen.resources.sanctions import AsyncSanctionsResource, SanctionsResource
from cryptascreen.resources.screening import AsyncScreeningResource, ScreeningResource
from cryptascreen.resources.settings import AsyncSettingsResource, SettingsResource
from cryptascreen.resources.webhooks import AsyncWebhooksResource, WebhooksResource
from cryptascreen.retry import async_execute_with_retry, execute_with_retry


def _parse(response: httpx.Response, binary: bool) -> Any:
    if binary:
        return response.content
    if response.status_code == 204 or not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


class HttpClient:
    """Synchronous HTTP client wrapper: auth headers, JSON, retry policy, error mapping."""

    def __init__(self, config: Config, transport: httpx.BaseTransport | None = None) -> None:
        self._config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            headers=config.get_headers(),
            timeout=config.timeout,
            transport=transport,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        headers: dict[str, str] | None = None,
        binary: bool = False,
    ) -> Any:
        """Send a request and return the parsed JSON (``None`` for an empty body, bytes when ``binary``)."""

        def _send() -> httpx.Response:
            return self._client.request(
                method, path, params=params or None, json=json, headers=headers
            )

        return _parse(execute_with_retry(self._config, _send), binary)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()


class AsyncHttpClient:
    """Asynchronous HTTP client wrapper."""

    def __init__(self, config: Config, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            headers=config.get_headers(),
            timeout=config.timeout,
            transport=transport,
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        headers: dict[str, str] | None = None,
        binary: bool = False,
    ) -> Any:
        """Send an async request and return the parsed JSON."""

        async def _send() -> httpx.Response:
            return await self._client.request(
                method, path, params=params or None, json=json, headers=headers
            )

        return _parse(await async_execute_with_retry(self._config, _send), binary)

    async def close(self) -> None:
        """Close the underlying async HTTP client."""
        await self._client.aclose()


def _config(
    api_key: str,
    base_url: str | None,
    timeout: float,
    max_retries: int,
    retry_base_delay: float,
) -> Config:
    if not api_key:
        raise ValueError("api_key is required")
    return Config(
        api_key=api_key,
        base_url=resolve_base_url(base_url),
        timeout=timeout,
        max_retries=max_retries,
        retry_base_delay=retry_base_delay,
    )


class CryptaScreen:
    """Synchronous CryptaScreen client.

    Usage::

        from cryptascreen import CryptaScreen

        client = CryptaScreen(api_key="csk_...")
        result = client.screening.screen_address({"address": "0x...", "chain": "ethereum"})

    Args:
        api_key: Your CryptaScreen API key.
        base_url: Base URL override (default: https://api.cryptascreen.com).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Maximum retries on 429 / 5xx (default: 3).
        retry_base_delay: Base backoff delay in seconds (default: 1).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_base_delay: float = 1.0,
    ) -> None:
        self._config = _config(api_key, base_url, timeout, max_retries, retry_base_delay)
        self._http = HttpClient(self._config)
        self.screening = ScreeningResource(self._http)
        self.sanctions = SanctionsResource(self._http)
        self.names = NamesResource(self._http)
        self.graph = GraphResource(self._http)
        self.cases = CasesResource(self._http)
        self.alerts = AlertsResource(self._http)
        self.compliance = ComplianceResource(self._http)
        self.intelligence = IntelligenceResource(self._http)
        self.webhooks = WebhooksResource(self._http)
        self.auth = AuthResource(self._http)
        self.capabilities = CapabilitiesResource(self._http)
        self.settings = SettingsResource(self._http)
        self.monitoring = MonitoringResource(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client and release resources."""
        self._http.close()

    def __enter__(self) -> CryptaScreen:  # noqa: PYI034
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()


class AsyncCryptaScreen:
    """Asynchronous CryptaScreen client (``async with AsyncCryptaScreen(api_key=...) as client``)."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_base_delay: float = 1.0,
    ) -> None:
        self._config = _config(api_key, base_url, timeout, max_retries, retry_base_delay)
        self._http = AsyncHttpClient(self._config)
        self.screening = AsyncScreeningResource(self._http)
        self.sanctions = AsyncSanctionsResource(self._http)
        self.names = AsyncNamesResource(self._http)
        self.graph = AsyncGraphResource(self._http)
        self.cases = AsyncCasesResource(self._http)
        self.alerts = AsyncAlertsResource(self._http)
        self.compliance = AsyncComplianceResource(self._http)
        self.intelligence = AsyncIntelligenceResource(self._http)
        self.webhooks = AsyncWebhooksResource(self._http)
        self.auth = AsyncAuthResource(self._http)
        self.capabilities = AsyncCapabilitiesResource(self._http)
        self.settings = AsyncSettingsResource(self._http)
        self.monitoring = AsyncMonitoringResource(self._http)

    async def close(self) -> None:
        """Close the underlying async HTTP client and release resources."""
        await self._http.close()

    async def __aenter__(self) -> AsyncCryptaScreen:  # noqa: PYI034
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()


CryptaScreenClient = CryptaScreen  # name of the TypeScript SDK class
