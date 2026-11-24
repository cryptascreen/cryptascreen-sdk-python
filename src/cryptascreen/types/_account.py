"""Models of the account, capability, settings and monitoring endpoints.

Responses are lenient (every field optional, unknown fields kept) like the other response models; request models
are strict about names.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from cryptascreen.types._models import CsModel


class AuthMe(CsModel):
    """``GET /auth/me``: the calling identity (an API key resolves to its tenant owner)."""

    id: str | None = None
    email: str | None = None
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    company_name: str | None = Field(default=None, alias="companyName")
    tier: str | None = None
    email_verified: bool | None = Field(default=None, alias="emailVerified")
    two_factor_enabled: bool | None = Field(default=None, alias="twoFactorEnabled")
    created_at: str | None = Field(default=None, alias="createdAt")
    platform_role: str | None = Field(default=None, alias="platformRole")
    tenant_id: str | None = Field(default=None, alias="tenantId")
    screening_role: str | None = Field(default=None, alias="screeningRole")
    data_region: str | None = Field(default=None, alias="dataRegion")
    auth_method: str | None = Field(default=None, alias="authMethod")
    legal_region: str | None = Field(default=None, alias="legalRegion")


class CapabilityChain(CsModel):
    """A chain the screening API accepts."""

    chain: str | None = None
    display_name: str | None = Field(default=None, alias="displayName")
    on_chain: str | None = Field(default=None, alias="onChain")
    sanctions_screenable: bool | None = Field(default=None, alias="sanctionsScreenable")


class CapabilityLayer(CsModel):
    """Live state of a screening layer."""

    layer: str | None = None
    state: str | None = None
    status: str | None = None
    sources: list[str] | None = None


class Capabilities(CsModel):
    """``GET /capabilities``."""

    chains: list[CapabilityChain] | None = None
    layers: list[CapabilityLayer] | None = None


class ScoreThresholdValues(CsModel):
    """Review / block thresholds."""

    review_at: int | None = Field(default=None, alias="reviewAt")
    block_at: int | None = Field(default=None, alias="blockAt")


class ScoreThresholdSettings(ScoreThresholdValues):
    """Tenant thresholds (defaults 40 / 70 until changed)."""

    source: str | None = None
    version: int | None = None
    defaults: ScoreThresholdValues | None = None
    updated_at: str | None = Field(default=None, alias="updatedAt")
    updated_by: str | None = Field(default=None, alias="updatedBy")


class ScoreThresholdAuditEntry(CsModel):
    """One change of the thresholds (action SET | RESET)."""

    changed_at: str | None = Field(default=None, alias="changedAt")
    actor: str | None = None
    action: str | None = None
    previous: ScoreThresholdValues | None = None
    current: ScoreThresholdValues | None = None
    version: int | None = None


class ScoreThresholdAuditPage(CsModel):
    """``GET /settings/score-thresholds/audit``."""

    items: list[ScoreThresholdAuditEntry] = Field(default_factory=list)


class NameMatchingStrength(CsModel):
    """Name-matching strength (CONSERVATIVE | BALANCED | STRICT)."""

    strength: str | None = None
    source: str | None = None
    version: int | None = None
    threshold: float | None = None
    updated_at: str | None = Field(default=None, alias="updatedAt")
    updated_by: str | None = Field(default=None, alias="updatedBy")
    options: list[str] | None = None


class ItemsResponse(CsModel):
    """A list wrapped as ``{"items": [...]}``; entries are open objects."""

    items: list[dict[str, Any]] = Field(default_factory=list)


class VendorKeyView(CsModel):
    """A customer-supplied vendor key as shown to the caller (last4 and fingerprint only, never the key)."""

    vendor: str | None = None
    display_name: str | None = Field(default=None, alias="displayName")
    configured: bool | None = None
    enabled: bool | None = None
    needs_secret: bool | None = Field(default=None, alias="needsSecret")
    last4: str | None = None
    fingerprint: str | None = None
    daily_cap: int | None = Field(default=None, alias="dailyCap")
    used_today: int | None = Field(default=None, alias="usedToday")
    last_test_at: str | None = Field(default=None, alias="lastTestAt")
    last_test_status: str | None = Field(default=None, alias="lastTestStatus")
    updated_at: str | None = Field(default=None, alias="updatedAt")


class MonitoredWallet(CsModel):
    """A wallet on the monitored list."""

    id: int | None = None
    address: str | None = None
    chain: str | None = None
    label: str | None = None
    added_at: str | None = Field(default=None, alias="addedAt")
    last_checked_at: str | None = Field(default=None, alias="lastCheckedAt")


class AddMonitoredWalletRequest(CsModel):
    """Body of ``monitoring.add_wallet``."""

    address: str
    chain: str
    label: str | None = None


class MonitoredName(CsModel):
    """A name saved to the monitored list (open object)."""


class BreachDetection(CsModel):
    """A breach detection."""

    id: int | None = None
    address: str | None = None
    chain: str | None = None
    breach_source: str | None = Field(default=None, alias="breachSource")
    breach_date: str | None = Field(default=None, alias="breachDate")
    severity: str | None = None
    description: str | None = None
    detected_at: str | None = Field(default=None, alias="detectedAt")
    acknowledged_at: str | None = Field(default=None, alias="acknowledgedAt")


class BreachSummary(CsModel):
    """Counts of breach detections."""

    unacknowledged_count: int | None = Field(default=None, alias="unacknowledgedCount")
    by_severity: dict[str, int] | None = Field(default=None, alias="bySeverity")
    total_breaches: int | None = Field(default=None, alias="totalBreaches")


class MonitoredNamesResponse(CsModel):
    """``GET /monitoring/names``."""

    items: list[dict[str, Any]] = Field(default_factory=list)
    used: int | None = None


class MonitoringOverview(CsModel):
    """``GET /monitoring/overview``."""

    names: list[dict[str, Any]] = Field(default_factory=list)
    wallets: list[dict[str, Any]] = Field(default_factory=list)
    name_hits: list[dict[str, Any]] = Field(default_factory=list, alias="nameHits")


class DeletedResponse(CsModel):
    """``{"deleted": true}``."""

    deleted: bool | None = None


class RemovedResponse(CsModel):
    """``{"removed": true}``."""

    removed: bool | None = None
