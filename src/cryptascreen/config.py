# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""SDK configuration."""

from __future__ import annotations

from dataclasses import dataclass, field

from cryptascreen._version import __version__

DEFAULT_BASE_URL = "https://api.cryptascreen.com"
# The one public host. It routes every request to the data region of the API key (csk_us_... / csk_eu_...).


def resolve_base_url(base_url: str | None) -> str:
    """Pick the API host: explicit ``base_url`` (local stack, proxy) or the default host."""
    return base_url or DEFAULT_BASE_URL


@dataclass(frozen=True)
class Config:
    """Configuration for the CryptaScreen SDK client.

    Attributes:
        api_key: Your CryptaScreen API key (``csk_...``).
        base_url: Base URL for the CryptaScreen API.
        timeout: Request timeout in seconds.
        max_retries: Maximum retries on 429 (not quota) and 5xx.
        retry_base_delay: Base delay in seconds for exponential backoff (1s, 2s, 4s ...).
        retry_max_delay: Maximum delay in seconds between retries.
    """

    api_key: str
    base_url: str = DEFAULT_BASE_URL
    timeout: float = 30.0
    max_retries: int = 3
    retry_base_delay: float = 1.0
    retry_max_delay: float = 30.0
    headers: dict[str, str] = field(default_factory=dict)

    def get_headers(self) -> dict[str, str]:
        """Return the full set of headers for API requests."""
        base = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"cryptascreen-python/{__version__}",
        }
        base.update(self.headers)
        return base
