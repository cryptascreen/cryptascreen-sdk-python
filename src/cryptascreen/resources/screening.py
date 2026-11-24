"""Screening resource (mirrors @cryptascreen/sdk screening endpoints)."""

from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any

from cryptascreen._util import (
    _body,
    _enc,
    _normalise_job_results,
    _query,
    _require_chain,
    _require_chains,
    generate_idempotency_key,
    is_terminal_job_status,
)
from cryptascreen.types._models import (
    BulkScreeningRequest,
    ScreenAddressRequest,
    ScreeningEvaluation,
    ScreeningEvaluationPage,
    ScreeningJob,
    ScreeningJobResultsPage,
    ScreeningResponse,
    WalletCounterpartyPage,
    WalletExposurePaths,
    WalletTransactionPage,
)

if TYPE_CHECKING:
    from cryptascreen.client import AsyncHttpClient, HttpClient


class ScreeningResource:
    """Synchronous screening operations. Access via ``client.screening``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def screen_address(self, request: ScreenAddressRequest | dict[str, Any]) -> ScreeningResponse:
        """POST /screen/address"""
        data = self._http.request(
            "POST", "/api/v1/screen/address", json=_require_chain(_body(request))
        )
        return ScreeningResponse.model_validate(data)

    def screen_bulk(
        self, request: BulkScreeningRequest | dict[str, Any]
    ) -> list[ScreeningResponse]:
        """Screen multiple addresses synchronously (max 1000). ``async`` is forced to False."""
        data = self._http.request(
            "POST", "/api/v1/screen/bulk", json={**_require_chains(_body(request)), "async": False}
        )
        return [ScreeningResponse.model_validate(x) for x in data]

    def screen_bulk_async(
        self, request: BulkScreeningRequest | dict[str, Any], *, idempotency_key: str | None = None
    ) -> ScreeningJob:
        """Submit a bulk screening job (max 10000). ``async`` is forced to True; an Idempotency-Key header is always sent."""
        headers = {"Idempotency-Key": idempotency_key or generate_idempotency_key()}
        data = self._http.request(
            "POST",
            "/api/v1/screen/bulk",
            json={**_require_chains(_body(request)), "async": True},
            headers=headers,
        )
        return ScreeningJob.model_validate(data)

    def poll_job(self, job_id: str) -> ScreeningJob:
        """GET /screen/jobs/{jobId}"""
        data = self._http.request("GET", f"/api/v1/screen/jobs/{_enc(job_id)}")
        return ScreeningJob.model_validate(data)

    def list_jobs(self) -> list[ScreeningJob]:
        """GET /screen/jobs"""
        data = self._http.request("GET", "/api/v1/screen/jobs")
        return [ScreeningJob.model_validate(x) for x in data]

    def get_job_results(
        self, job_id: str, *, page: int = 0, size: int = 100
    ) -> ScreeningJobResultsPage:
        """One page (0-based, size 1..1000) of a job's stored per-address items."""
        data = self._http.request(
            "GET",
            f"/api/v1/screen/jobs/{_enc(job_id)}/results",
            params={"page": page, "size": size},
        )
        return _normalise_job_results(data, job_id, page, size)

    def cancel_job(self, job_id: str) -> ScreeningJob:
        """POST /screen/jobs/{jobId}/cancel"""
        data = self._http.request("POST", f"/api/v1/screen/jobs/{_enc(job_id)}/cancel")
        return ScreeningJob.model_validate(data)

    def get_history(self, chain: str, address: str) -> ScreeningResponse:
        """GET /screen/address/{chain}/{address}/history"""
        data = self._http.request(
            "GET", f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/history"
        )
        return ScreeningResponse.model_validate(data)

    def list_evaluations(
        self, chain: str, address: str, *, page: int = 0, size: int = 20
    ) -> ScreeningEvaluationPage:
        """GET /screen/address/{chain}/{address}/evaluations"""
        data = self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/evaluations",
            params=_query(page=page, size=size),
        )
        return ScreeningEvaluationPage.model_validate(data)

    def get_counterparties(
        self,
        chain: str,
        address: str,
        *,
        page: int | None = None,
        size: int | None = None,
        sort: str | None = None,
        order: str | None = None,
        days: int | None = None,
        direction: str | None = None,
        listed_only: bool | None = None,
    ) -> WalletCounterpartyPage:
        """GET /screen/address/{chain}/{address}/counterparties"""
        data = self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/counterparties",
            params=_query(
                page=page,
                size=size,
                sort=sort,
                order=order,
                days=days,
                direction=direction,
                listedOnly=listed_only,
            ),
        )
        return WalletCounterpartyPage.model_validate(data)

    def get_transactions(
        self,
        chain: str,
        address: str,
        *,
        page: int | None = None,
        size: int | None = None,
        sort: str | None = None,
        order: str | None = None,
        days: int | None = None,
        direction: str | None = None,
        counterparty: str | None = None,
    ) -> WalletTransactionPage:
        """GET /screen/address/{chain}/{address}/transactions"""
        data = self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/transactions",
            params=_query(
                page=page,
                size=size,
                sort=sort,
                order=order,
                days=days,
                direction=direction,
                counterparty=counterparty,
            ),
        )
        return WalletTransactionPage.model_validate(data)

    def get_exposure_paths(
        self, chain: str, address: str, *, days: int | None = None
    ) -> WalletExposurePaths:
        """GET /screen/address/{chain}/{address}/exposure-paths"""
        data = self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/exposure-paths",
            params=_query(days=days),
        )
        return WalletExposurePaths.model_validate(data)

    def get_evaluation(self, evaluation_id: str) -> ScreeningEvaluation:
        """GET /screen/evaluations/{evaluationId}"""
        data = self._http.request("GET", f"/api/v1/screen/evaluations/{_enc(evaluation_id)}")
        return ScreeningEvaluation.model_validate(data)

    def screen_bulk_and_wait(
        self,
        request: BulkScreeningRequest | dict[str, Any],
        poll_interval: float = 2.0,
        timeout: float = 300.0,
        *,
        idempotency_key: str | None = None,
    ) -> ScreeningJob:
        """Submit a bulk job and poll until a terminal status (COMPLETED | PARTIAL | FAILED | CANCELLED)."""
        job = self.screen_bulk_async(request, idempotency_key=idempotency_key)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            status = self.poll_job(job.job_id or "")
            if is_terminal_job_status(status.status):
                return status
            time.sleep(poll_interval)
        raise TimeoutError(f"Screening job {job.job_id} did not complete within {timeout}s")


class AsyncScreeningResource:
    """Asynchronous screening operations. Access via ``client.screening``."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def screen_address(
        self, request: ScreenAddressRequest | dict[str, Any]
    ) -> ScreeningResponse:
        """POST /screen/address"""
        data = await self._http.request(
            "POST", "/api/v1/screen/address", json=_require_chain(_body(request))
        )
        return ScreeningResponse.model_validate(data)

    async def screen_bulk(
        self, request: BulkScreeningRequest | dict[str, Any]
    ) -> list[ScreeningResponse]:
        """Screen multiple addresses synchronously (max 1000). ``async`` is forced to False."""
        data = await self._http.request(
            "POST", "/api/v1/screen/bulk", json={**_require_chains(_body(request)), "async": False}
        )
        return [ScreeningResponse.model_validate(x) for x in data]

    async def screen_bulk_async(
        self, request: BulkScreeningRequest | dict[str, Any], *, idempotency_key: str | None = None
    ) -> ScreeningJob:
        """Submit a bulk screening job (max 10000). ``async`` is forced to True; an Idempotency-Key header is always sent."""
        headers = {"Idempotency-Key": idempotency_key or generate_idempotency_key()}
        data = await self._http.request(
            "POST",
            "/api/v1/screen/bulk",
            json={**_require_chains(_body(request)), "async": True},
            headers=headers,
        )
        return ScreeningJob.model_validate(data)

    async def poll_job(self, job_id: str) -> ScreeningJob:
        """GET /screen/jobs/{jobId}"""
        data = await self._http.request("GET", f"/api/v1/screen/jobs/{_enc(job_id)}")
        return ScreeningJob.model_validate(data)

    async def list_jobs(self) -> list[ScreeningJob]:
        """GET /screen/jobs"""
        data = await self._http.request("GET", "/api/v1/screen/jobs")
        return [ScreeningJob.model_validate(x) for x in data]

    async def get_job_results(
        self, job_id: str, *, page: int = 0, size: int = 100
    ) -> ScreeningJobResultsPage:
        """One page (0-based, size 1..1000) of a job's stored per-address items."""
        data = await self._http.request(
            "GET",
            f"/api/v1/screen/jobs/{_enc(job_id)}/results",
            params={"page": page, "size": size},
        )
        return _normalise_job_results(data, job_id, page, size)

    async def cancel_job(self, job_id: str) -> ScreeningJob:
        """POST /screen/jobs/{jobId}/cancel"""
        data = await self._http.request("POST", f"/api/v1/screen/jobs/{_enc(job_id)}/cancel")
        return ScreeningJob.model_validate(data)

    async def get_history(self, chain: str, address: str) -> ScreeningResponse:
        """GET /screen/address/{chain}/{address}/history"""
        data = await self._http.request(
            "GET", f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/history"
        )
        return ScreeningResponse.model_validate(data)

    async def list_evaluations(
        self, chain: str, address: str, *, page: int = 0, size: int = 20
    ) -> ScreeningEvaluationPage:
        """GET /screen/address/{chain}/{address}/evaluations"""
        data = await self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/evaluations",
            params=_query(page=page, size=size),
        )
        return ScreeningEvaluationPage.model_validate(data)

    async def get_counterparties(
        self,
        chain: str,
        address: str,
        *,
        page: int | None = None,
        size: int | None = None,
        sort: str | None = None,
        order: str | None = None,
        days: int | None = None,
        direction: str | None = None,
        listed_only: bool | None = None,
    ) -> WalletCounterpartyPage:
        """GET /screen/address/{chain}/{address}/counterparties"""
        data = await self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/counterparties",
            params=_query(
                page=page,
                size=size,
                sort=sort,
                order=order,
                days=days,
                direction=direction,
                listedOnly=listed_only,
            ),
        )
        return WalletCounterpartyPage.model_validate(data)

    async def get_transactions(
        self,
        chain: str,
        address: str,
        *,
        page: int | None = None,
        size: int | None = None,
        sort: str | None = None,
        order: str | None = None,
        days: int | None = None,
        direction: str | None = None,
        counterparty: str | None = None,
    ) -> WalletTransactionPage:
        """GET /screen/address/{chain}/{address}/transactions"""
        data = await self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/transactions",
            params=_query(
                page=page,
                size=size,
                sort=sort,
                order=order,
                days=days,
                direction=direction,
                counterparty=counterparty,
            ),
        )
        return WalletTransactionPage.model_validate(data)

    async def get_exposure_paths(
        self, chain: str, address: str, *, days: int | None = None
    ) -> WalletExposurePaths:
        """GET /screen/address/{chain}/{address}/exposure-paths"""
        data = await self._http.request(
            "GET",
            f"/api/v1/screen/address/{_enc(chain)}/{_enc(address)}/exposure-paths",
            params=_query(days=days),
        )
        return WalletExposurePaths.model_validate(data)

    async def get_evaluation(self, evaluation_id: str) -> ScreeningEvaluation:
        """GET /screen/evaluations/{evaluationId}"""
        data = await self._http.request("GET", f"/api/v1/screen/evaluations/{_enc(evaluation_id)}")
        return ScreeningEvaluation.model_validate(data)

    async def screen_bulk_and_wait(
        self,
        request: BulkScreeningRequest | dict[str, Any],
        poll_interval: float = 2.0,
        timeout: float = 300.0,
        *,
        idempotency_key: str | None = None,
    ) -> ScreeningJob:
        """Submit a bulk job and poll until a terminal status (COMPLETED | PARTIAL | FAILED | CANCELLED)."""
        job = await self.screen_bulk_async(request, idempotency_key=idempotency_key)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            status = await self.poll_job(job.job_id or "")
            if is_terminal_job_status(status.status):
                return status
            await asyncio.sleep(poll_interval)
        raise TimeoutError(f"Screening job {job.job_id} did not complete within {timeout}s")
