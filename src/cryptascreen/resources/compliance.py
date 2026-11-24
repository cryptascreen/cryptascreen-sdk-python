"""Compliance resource (mirrors @cryptascreen/sdk compliance endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptascreen._util import _body, _enc
from cryptascreen.errors import ValidationError
from cryptascreen.types._models import (
    Dac8ReportRequest,
    Dac8ReportResult,
    TravelRuleCheckRequest,
    TravelRuleCheckResult,
    TravelRulePayload,
    TravelRulePayloadRequest,
    VaspIdentification,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class ComplianceResource:
    """Synchronous compliance operations. Access via ``client.compliance``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def check_travel_rule(
        self, request: TravelRuleCheckRequest | dict[str, Any]
    ) -> TravelRuleCheckResult:
        """POST /compliance/travel-rule/check"""
        data = self._http.request(
            "POST", "/api/v1/compliance/travel-rule/check", json=_body(request)
        )
        return TravelRuleCheckResult.model_validate(data)

    def build_travel_rule_payload(
        self, request: TravelRulePayloadRequest | dict[str, Any]
    ) -> TravelRulePayload:
        """POST /compliance/travel-rule/payload"""
        data = self._http.request(
            "POST", "/api/v1/compliance/travel-rule/payload", json=_body(request)
        )
        return TravelRulePayload.model_validate(data)

    def identify_vasp(self, chain: str, address: str) -> VaspIdentification:
        """GET /compliance/travel-rule/vasp/identify/{chain}/{address}"""
        data = self._http.request(
            "GET", f"/api/v1/compliance/travel-rule/vasp/identify/{_enc(chain)}/{_enc(address)}"
        )
        return VaspIdentification.model_validate(data)

    def generate_dac8_report(self, request: Dac8ReportRequest | dict[str, Any]) -> Dac8ReportResult:
        """Deprecated: DAC8 reporting is deferred (unvalidated draft, not a filing). A request of the 0.1.x shape raises ValidationError client-side."""
        body = _body(request)
        missing = [
            k for k in ("taxYear", "jurisdiction", "operator", "users") if body.get(k) is None
        ]
        if missing:
            raise ValidationError(
                f"DAC8 report request requires {', '.join(missing)} (DAC8 is deferred; see CHANGELOG)",
                {k: ["required"] for k in missing},
                validation_code="DAC8_REQUEST_SHAPE",
            )
        data = self._http.request("POST", "/api/v1/compliance/dac8/report", json=body)
        return Dac8ReportResult.model_validate(data)


class AsyncComplianceResource:
    """Asynchronous compliance operations. Access via ``client.compliance``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def check_travel_rule(
        self, request: TravelRuleCheckRequest | dict[str, Any]
    ) -> TravelRuleCheckResult:
        """POST /compliance/travel-rule/check"""
        data = await self._http.request(
            "POST", "/api/v1/compliance/travel-rule/check", json=_body(request)
        )
        return TravelRuleCheckResult.model_validate(data)

    async def build_travel_rule_payload(
        self, request: TravelRulePayloadRequest | dict[str, Any]
    ) -> TravelRulePayload:
        """POST /compliance/travel-rule/payload"""
        data = await self._http.request(
            "POST", "/api/v1/compliance/travel-rule/payload", json=_body(request)
        )
        return TravelRulePayload.model_validate(data)

    async def identify_vasp(self, chain: str, address: str) -> VaspIdentification:
        """GET /compliance/travel-rule/vasp/identify/{chain}/{address}"""
        data = await self._http.request(
            "GET", f"/api/v1/compliance/travel-rule/vasp/identify/{_enc(chain)}/{_enc(address)}"
        )
        return VaspIdentification.model_validate(data)

    async def generate_dac8_report(
        self, request: Dac8ReportRequest | dict[str, Any]
    ) -> Dac8ReportResult:
        """Deprecated: DAC8 reporting is deferred (unvalidated draft, not a filing). A request of the 0.1.x shape raises ValidationError client-side."""
        body = _body(request)
        missing = [
            k for k in ("taxYear", "jurisdiction", "operator", "users") if body.get(k) is None
        ]
        if missing:
            raise ValidationError(
                f"DAC8 report request requires {', '.join(missing)} (DAC8 is deferred; see CHANGELOG)",
                {k: ["required"] for k in missing},
                validation_code="DAC8_REQUEST_SHAPE",
            )
        data = await self._http.request("POST", "/api/v1/compliance/dac8/report", json=body)
        return Dac8ReportResult.model_validate(data)
