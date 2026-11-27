# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Cases resource (mirrors @cryptascreen/sdk cases endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptascreen._util import _body, _enc, _query
from cryptascreen.types._models import (
    AddEvidenceRequest,
    AddNoteRequest,
    CaseAssignment,
    CaseEvidence,
    CaseNote,
    CreateCaseRequest,
    EscalateCaseRequest,
    InvestigationCase,
    PaginatedResponse,
    UpdateCaseStatusRequest,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class CasesResource:
    """Synchronous cases operations. Access via ``client.cases``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, request: CreateCaseRequest | dict[str, Any]) -> InvestigationCase:
        """POST /cases"""
        data = self._http.request("POST", "/api/v1/cases", json=_body(request))
        return InvestigationCase.model_validate(data)

    def list(
        self,
        *,
        status: str | None = None,
        priority: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> PaginatedResponse[InvestigationCase]:
        """GET /cases"""
        data = self._http.request(
            "GET",
            "/api/v1/cases",
            params=_query(status=status, priority=priority, page=page, pageSize=page_size),
        )
        return PaginatedResponse[InvestigationCase].model_validate(data)

    def get(self, case_id: str) -> InvestigationCase:
        """GET /cases/{caseId}"""
        data = self._http.request("GET", f"/api/v1/cases/{_enc(case_id)}")
        return InvestigationCase.model_validate(data)

    def update_status(
        self, case_id: str, request: UpdateCaseStatusRequest | dict[str, Any]
    ) -> InvestigationCase:
        """PUT /cases/{caseId}/status"""
        data = self._http.request(
            "PUT", f"/api/v1/cases/{_enc(case_id)}/status", json=_body(request)
        )
        return InvestigationCase.model_validate(data)

    def add_note(self, case_id: str, request: AddNoteRequest | dict[str, Any]) -> CaseNote:
        """POST /cases/{caseId}/notes"""
        data = self._http.request(
            "POST", f"/api/v1/cases/{_enc(case_id)}/notes", json=_body(request)
        )
        return CaseNote.model_validate(data)

    def add_evidence(
        self, case_id: str, request: AddEvidenceRequest | dict[str, Any]
    ) -> CaseEvidence:
        """POST /cases/{caseId}/evidence"""
        data = self._http.request(
            "POST", f"/api/v1/cases/{_enc(case_id)}/evidence", json=_body(request)
        )
        return CaseEvidence.model_validate(data)

    def escalate(
        self, case_id: str, request: EscalateCaseRequest | dict[str, Any]
    ) -> InvestigationCase:
        """POST /cases/{caseId}/escalate"""
        data = self._http.request(
            "POST", f"/api/v1/cases/{_enc(case_id)}/escalate", json=_body(request)
        )
        return InvestigationCase.model_validate(data)

    def get_assignment(self, case_id: str) -> CaseAssignment:
        """GET /cases/{caseId}/assignment"""
        data = self._http.request("GET", f"/api/v1/cases/{_enc(case_id)}/assignment")
        return CaseAssignment.model_validate(data)

    def set_assignee(self, case_id: str, user_id: int | None) -> CaseAssignment:
        """Assign the case to a user of your organization, or unassign with ``None``."""
        data = self._http.request(
            "PUT", f"/api/v1/cases/{_enc(case_id)}/assignee", json={"userId": user_id}
        )
        return CaseAssignment.model_validate(data)

    def link_evaluation(self, case_id: str, evaluation_id: str) -> CaseAssignment:
        """Link a screening evaluation of your organization to the case (idempotent)."""
        data = self._http.request(
            "POST",
            f"/api/v1/cases/{_enc(case_id)}/evaluations",
            json={"evaluationId": evaluation_id},
        )
        return CaseAssignment.model_validate(data)


class AsyncCasesResource:
    """Asynchronous cases operations. Access via ``client.cases``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def create(self, request: CreateCaseRequest | dict[str, Any]) -> InvestigationCase:
        """POST /cases"""
        data = await self._http.request("POST", "/api/v1/cases", json=_body(request))
        return InvestigationCase.model_validate(data)

    async def list(
        self,
        *,
        status: str | None = None,
        priority: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> PaginatedResponse[InvestigationCase]:
        """GET /cases"""
        data = await self._http.request(
            "GET",
            "/api/v1/cases",
            params=_query(status=status, priority=priority, page=page, pageSize=page_size),
        )
        return PaginatedResponse[InvestigationCase].model_validate(data)

    async def get(self, case_id: str) -> InvestigationCase:
        """GET /cases/{caseId}"""
        data = await self._http.request("GET", f"/api/v1/cases/{_enc(case_id)}")
        return InvestigationCase.model_validate(data)

    async def update_status(
        self, case_id: str, request: UpdateCaseStatusRequest | dict[str, Any]
    ) -> InvestigationCase:
        """PUT /cases/{caseId}/status"""
        data = await self._http.request(
            "PUT", f"/api/v1/cases/{_enc(case_id)}/status", json=_body(request)
        )
        return InvestigationCase.model_validate(data)

    async def add_note(self, case_id: str, request: AddNoteRequest | dict[str, Any]) -> CaseNote:
        """POST /cases/{caseId}/notes"""
        data = await self._http.request(
            "POST", f"/api/v1/cases/{_enc(case_id)}/notes", json=_body(request)
        )
        return CaseNote.model_validate(data)

    async def add_evidence(
        self, case_id: str, request: AddEvidenceRequest | dict[str, Any]
    ) -> CaseEvidence:
        """POST /cases/{caseId}/evidence"""
        data = await self._http.request(
            "POST", f"/api/v1/cases/{_enc(case_id)}/evidence", json=_body(request)
        )
        return CaseEvidence.model_validate(data)

    async def escalate(
        self, case_id: str, request: EscalateCaseRequest | dict[str, Any]
    ) -> InvestigationCase:
        """POST /cases/{caseId}/escalate"""
        data = await self._http.request(
            "POST", f"/api/v1/cases/{_enc(case_id)}/escalate", json=_body(request)
        )
        return InvestigationCase.model_validate(data)

    async def get_assignment(self, case_id: str) -> CaseAssignment:
        """GET /cases/{caseId}/assignment"""
        data = await self._http.request("GET", f"/api/v1/cases/{_enc(case_id)}/assignment")
        return CaseAssignment.model_validate(data)

    async def set_assignee(self, case_id: str, user_id: int | None) -> CaseAssignment:
        """Assign the case to a user of your organization, or unassign with ``None``."""
        data = await self._http.request(
            "PUT", f"/api/v1/cases/{_enc(case_id)}/assignee", json={"userId": user_id}
        )
        return CaseAssignment.model_validate(data)

    async def link_evaluation(self, case_id: str, evaluation_id: str) -> CaseAssignment:
        """Link a screening evaluation of your organization to the case (idempotent)."""
        data = await self._http.request(
            "POST",
            f"/api/v1/cases/{_enc(case_id)}/evaluations",
            json={"evaluationId": evaluation_id},
        )
        return CaseAssignment.model_validate(data)
