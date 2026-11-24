"""Webhooks resource: reading webhook endpoints and their deliveries with an API key.

Registering, deleting and test-sending a webhook endpoint require a signed-in user in the CryptaScreen app; an API key
is refused (403), so this SDK does not offer them.
"""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from cryptascreen._util import _enc
from cryptascreen.types._models import (
    WebhookConfig,
    WebhookDelivery,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class WebhooksResource:
    """Synchronous webhooks operations. Access via ``client.webhooks``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> list[WebhookConfig]:
        """GET /webhooks"""
        data = self._http.request("GET", "/api/v1/webhooks")
        return [WebhookConfig.model_validate(x) for x in data]

    def get_deliveries(self, webhook_id: int | str) -> builtins.list[WebhookDelivery]:
        """The last 50 deliveries of an endpoint, newest first (404 for another tenant's endpoint)."""
        data = self._http.request("GET", f"/api/v1/webhooks/{_enc(str(webhook_id))}/deliveries")
        return [WebhookDelivery.model_validate(x) for x in data]


class AsyncWebhooksResource:
    """Asynchronous webhooks operations. Access via ``client.webhooks``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> list[WebhookConfig]:
        """GET /webhooks"""
        data = await self._http.request("GET", "/api/v1/webhooks")
        return [WebhookConfig.model_validate(x) for x in data]

    async def get_deliveries(self, webhook_id: int | str) -> builtins.list[WebhookDelivery]:
        """The last 50 deliveries of an endpoint, newest first (404 for another tenant's endpoint)."""
        data = await self._http.request(
            "GET", f"/api/v1/webhooks/{_enc(str(webhook_id))}/deliveries"
        )
        return [WebhookDelivery.model_validate(x) for x in data]
